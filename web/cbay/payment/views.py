import json
import uuid

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.base import TemplateView

from basket.basket import Basket
from account.models import UserBase
from orders.models import Order, OrderItem
from store.models import Product
import logging 

logger = logging.getLogger("django")

from orders.views import payment_confirmation

from django.core.cache import cache

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.conf import settings

import pandas as pd
from payment.models import Intent

import requests
from .cc import create_named_payment_address, get_wallet

from orders.forms import OrderForm

def generate_order_markdown(basket, order, request):
    order_list = []
    for (k, v) in basket.basket.items():
        product = Product.objects.filter(pk=k)[0]
        order_list.append(
            {
                "Quantity": v["quantity"],
                "Product": product.subtitle,
                "Unit price": f"£ {v['price']}",
            }
        )
    order_table = pd.DataFrame.from_records(order_list).to_markdown(
        tablefmt="grid", index=False
    )
    order_detail_list = [{"order_id": order.id, "customer_id": request.user.id}]
    order_detail_table = pd.DataFrame.from_records(order_detail_list).to_markdown(
        tablefmt="grid", index=False
    )
    return order_table, order_detail_table

def get_xrate():
    logger.info("Retriving exhange rate from:")
    key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCGBP"
    logger.info(key)
    data = requests.get(key)
    return float(data.json()["price"]) 

def generate_payment_address(fiat_value, order):
    # Hit API for current btc to gbp exchange price.
    # logger.info("Attempting to retrieve Retriving exchange rate from cache ... ")
    # BTC_X_RATE = cache.get("BTC_X_RATE")
    # logger.info(f"Cache return: {BTC_X_RATE}")
    # if BTC_X_RATE is None: 
    BTC_X_RATE = get_xrate()

    crypto_value = BTC_X_RATE ** (-1) * float(fiat_value)

    server_wallet = get_wallet(scan=False)

    kid, server_wallet = create_named_payment_address(
        wallet=server_wallet, address_name=order.order_key
    )
    payment_address = server_wallet.key(kid).address
    return payment_address, crypto_value


@login_required
def order_placed(request):
    basket = Basket(request)

    user = UserBase.objects.filter(pk=request.user.id)[0]

    order = Order.objects.filter(user_id=request.user.id).latest("created")

    fiat_value = order.total_paid
    order_table, order_detail_table = generate_order_markdown(basket, order, request)
    basket.clear()
    #######################################################################################
    # Crypto payment
    #######################################################################################

    payment_address, crypto_value = generate_payment_address(fiat_value, order)

    intent = Intent.objects.create(
        order=order,
        order_key=order.order_key,
        email=user.email,
        payment_address=payment_address,
        total_amount=crypto_value,
        paid_amount=0.0,
    )
    intent.save()

    subject = "Neuropharma: Bitcoin payment invoice"
    message = render_to_string(
        "payment/email.html",
        {
            "user": user,
            "order_details": order_detail_table,
            "order_table": order_table,
            "order": order,
            "fiat_value": fiat_value,
            "payment_address": payment_address,
            "crypto_value": round(crypto_value, 6),
        },
    )
    user.email_user(subject=subject, message=message)

    return render(request, "payment/orderplaced.html")


class Error(TemplateView):
    template_name = "payment/error.html"


@login_required
def BasketView(request):

    import uuid 
    context = {
        "form": OrderForm(initial={"order_key":str(uuid.uuid4())}),
        }
    return render(
        request, "payment/home.html", context=context
    )
