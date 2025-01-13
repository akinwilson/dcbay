# from time import sleep
# from django.core.mail import send_mail
from celery import shared_task
from django.core.cache import cache
from celery.utils.log import get_task_logger
import requests
import logging 

logger = logging.getLogger("django")
from django.conf import settings

from payment.models import Intent
from orders.models import Order, OrderItem
import decimal
from decimal import Decimal
from .cc import get_wallet


from django.template.loader import render_to_string
from django.core.mail import send_mail


# https://testdriven.io/blog/django-celery-periodic-tasks/


def check_intent_update_order_email_user(order_key):
    '''
    get Order and Intent 

    check intent for total amount at address

    if has payment received, update the Order 
    '''
    intent = Intent.objects.filter(order_key=order_key)[0]
    order = Order.objects.filter(order_key=order_key)[0]

    wallet = get_wallet(scan=True)
    key_id_named_addresses = dict(
        [(x.name, x.id) for x in wallet.keys() if x.name == order_key]
    )
    kid = key_id_named_addresses[order_key]
    logger.info(f"Key id for order_key: {order_key}")
    logger.info(f"key_id: {kid}")
    # scan for new tx and update wallet
    new_tx  = wallet.scan_key(kid)
    logger.info(f"scanned key with id: {kid}")
    logger.info(f"Were there new transactions found from the last scan?-{ 'yes' if new_tx else 'no' }")
    # UPDATE INTENT WITH AMOUNT AT ADRRESS AS BITCOIN WALLET DETERMINES
    satoshis = wallet.key(kid)._balance
    logger.info(f"type of wallet ballance {satoshis}:{type(satoshis)}")

    received_amount = Decimal(int(satoshis) * 10e-9)  # from satoshis to tbtc type Decimal

    
    logger.info(f"Converted to decimal type and units of BTC: {received_amount}")
    logger.info(f"Amount found at address {wallet.key(kid).address}: {received_amount}BTC")
    expected_amount = intent.total_amount  # decimal amount expect
    logger.info("Updating intent with amount found at address")
    # update intent 
    if received_amount >= intent.paid_amount:
        # the paid_amount is preset to zero, overwriten from values in keys, if non-zero value is recorded, mostly the payment and over writes 
        # but after sweeping, the keys will read zero BTC, and we dont want to overwrite the previously recorded non-zero value. 
        intent.paid_amount=received_amount
    else: 
        logger.info(f"Intent: {intent} has had paid amount already recorded which i greater than the re-recorded amount at key")
        logger.info(f"Intents paid amount: {intent.paid_amount}")
        logger.info(f"Receied from key scan: {received_amount}")
        logger.info(f"Total amount POSSIBLY received the sum: {received_amount + intent.paid_amount } but already swept the keys")
        logger.info(f"It may be helpful to scan the address: {wallet.key(kid).address} for total amount paid and the amount supposed to be paid")
        logger.info("*****Implications******")
        logger.info(f"Someone has attempt to make an additional payment to the address: {wallet.key(kid).address}")
        logger.info("But the key has already been swept, and this will appear as an under payment")
        logger.info(f"Order key: {order_key}")
        logger.info("OPTIONS:")
        logger.info("1) Add the newly recorded received amount to the paid_amount, and save the intent")
        logger.info("----> intent.paid_amount = intent.paid_amount+received_amount")
        logger.info("2) Manually update the corresponding order.billing_status=True intent.paid=True and send the user an email confirming their payment")
        logger.info("----> This would normally mean you found these logs because someone has contacted you because they never received their shipping")
        logger.info("----> the shipping address email only goes out if the below conditions of has_paid = True and intent.paid = False ")
        logger.info("CURRENTLY:")
        logger.info("=======we are in option 2===========")
        logger.info("do not overwrite intent.paid_amount UNLESS the received amount is greater than the currrent, pre-set 0.0 value, but possibly previously recorded payment of none-zero")
        logger.info("could be mistaken for additional payment of and under-paid order")
        # intent.paid_amount = intent.paid_amount+received_amount

    val_diff =  expected_amount - received_amount 
    logger.info(f"Payment difference: {val_diff} BTC")

    precentage_diff = val_diff / expected_amount
    logger.info(f"Payment precentage difference: {precentage_diff*100} %")
    logger.info(f"Allowed precentage differnce :{float(settings.PAYMENT_PRECENTAGE_LEEWAY) *100:.2f}%")


    if precentage_diff <= Decimal(0.0):
        # over payment
        logger.info("Over payment. Sending payment confirmation")
        has_paid = True

    elif (precentage_diff > Decimal(0.0)) and (abs(precentage_diff) <= Decimal(settings.PAYMENT_PRECENTAGE_LEEWAY)):
        # under payment within leeway
        logger.info(f"under payment within leeway of < {Decimal(settings.PAYMENT_PRECENTAGE_LEEWAY)}")
        has_paid = True
    
    elif (precentage_diff > Decimal(0.0)) and (abs(precentage_diff) > Decimal(settings.PAYMENT_PRECENTAGE_LEEWAY)):
        # under payment outside leeway check_intent_update_order_email_user
        logger.info(f"under payment outside leeway > {Decimal(settings.PAYMENT_PRECENTAGE_LEEWAY)} ")
        has_paid = False
        logger.info("Notify underpayment ... ")

    logger.info(f"Has the intent been furfilled by customer? { 'YES' if has_paid else 'NO'}")

    if has_paid and not intent.paid == True:
        logger.info("Sending confirmation email")
        # Payment received and previously has not 
        # been recorded that payment received
        order.billing_status=True
        intent.paid=True
        order.save()
        intent.save()
        message = render_to_string(
            "payment/payment_confirmation.html",
            {"user": order.user, "order_id": order.id},
        )
        subject = "Neuropharma: Payment received!"
        logger.info(f"Sending payment confirmation email for order order_id: { order.id}")
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [intent.email],
            fail_silently=False,
        )



@shared_task
def payment_confirmations():
    # Checking if invoices have been paid
    logger.info("payment confirmation routine starting...")
    intents = Intent.objects.filter(paid=False, expired=False)
    logger.info(f"Number of unpaid intents {len(intents)}")
    for intent in intents:
        check_intent_update_order_email_user(intent.order_key)

@shared_task
def daily_shipments():
    '''
    generate shipment address and update order status to shipped
    '''
    logger.info("Collating daily shipments ... ")
    email_content = []
    orders = Order.objects.filter(billing_status=True, shipped=False)
    logger.info(f"Number of orders with completed payment but not shipped: {len(orders)}")
    if len(orders) == 0:
        logger.info("No orders to be shipped")
    else: 
        logger.info("Collating shipping addresses")
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            qts = []
            for order_item in order_items:
                qts.append(f"{order_item.product}|{order_item.quantity}")
                shipping_address = f"\n{order.first_name} {order.last_name}\n{order.address1}\n{order.post_code}\n{ order.city }\n{ order.county }\n{ order.country }\n\n"
                qts.append(shipping_address)

            email_content.append("".join(qts))

        message = "".join(email_content)
        subject = "DAILY SHIPMENTS"
        send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        # mark orders that have had addresses emailed to admin as shipped
        if len(orders)>0:
            logger.info("Updating the shipped check_intent_update_order_email_user of orders")
        for order in orders:
            order.shipped = True 
            order.save()


@shared_task
def daily_bitcoin_exchange_rate():
    '''
    Function supposed to retrieve bitcoin exchange rate and store in cache
    '''
    logger.info("Retrieving BTC exchange rate from API to set as cached value")
    key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCGBP"
    logger.info(key)
    data = requests.get(key)
    btc_exhange_rate = float(data.json()["price"])
    logger.info(f"Setting cache key BTC_X_RATE to value: {btc_exhange_rate}")
    cache.set("BTC_X_RATE", btc_exhange_rate, timeout=None)
    btc_x_rate_from_cache = cache.get("BTC_X_RATE")
    logger.info(f"Value returned by cache in shared_task: {btc_x_rate_from_cache}")
    



# # @shared_task
# # def transfer_funds():
# #     """
# #     function sends funds to main wallet
# #     """
# #     orders = Order.objects.filter(billing_status=True, shipped=True, transferred=False)
# #     logger.info(f"Transfering funds for completed orders: {orders}")
    
    
# #     for order in orders:
# #         transfer_fund(order)


# def get_sweepable_key(order):
#     '''
#     transfer to main wallet from webserver 
#     '''
#     # intent.update(transferred=True)
#     wallet = get_wallet(scan=False)
#     order_key = order.order_key
#     key_id_named_addresses = dict(
#         [(x.name, x.id) for x in wallet.keys() if x.name == order_key]
#     )
#     kid = key_id_named_addresses[order_key]
#     return wallet.key(kid).address


#     logger.info(f"scaning address: {wallet.key(kid).address} for new txs and updating wallet")
#     wallet.scan_key(kid)

#     logger.info(f"Sending to main wallet address: {settings.OFFLINE_WALLET_ADDRESS}")
#     tx = send_to_main_wallet(wallet, kid)
#     logger.info("Transcation:")
#     logger.info(tx.as_dict())
#     order.transferred = True 
#     order.save()

