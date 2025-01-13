from django.conf import settings
from bitcoinlib.wallets import wallet_exists, Wallet
import logging 
from bitcoinlib.wallets import WalletError
from payment.models import Intent
from orders.models import Order
from decimal import Decimal

logger = logging.getLogger("django")



def get_wallet(scan=True):
    '''
    loads OR creates wallet based on settings
    '''
    db_creds = settings.DATABASES["crypto"]
    db_uri = f"postgresql://{db_creds['USER']}:{db_creds['PASSWORD']}@{db_creds['HOST']}:{db_creds['PORT']}/{db_creds['NAME']}"

    if wallet_exists(settings.SERVER_WALLET_NAME, db_uri=db_uri):
        logger.info(f"Loading wallet based on name: {settings.SERVER_WALLET_NAME} for network {settings.PAYMENT_NETWORK}")
        server_wallet = Wallet(settings.SERVER_WALLET_NAME, db_uri=db_uri)
    else:
        logger.info(f"Creating wallet with name {settings.SERVER_WALLET_NAME} using private mnemonic for network {settings.PAYMENT_NETWORK}")
        server_wallet = Wallet.create(
            keys=settings.PRIVATE_MNEMONIC,
            network=settings.PAYMENT_NETWORK,
            name=settings.SERVER_WALLET_NAME,
            db_uri=db_uri,
        )
    if scan:

        logger.info(f"Scanning wallet {settings.SERVER_WALLET_NAME} ... ")
        txs = server_wallet.transactions_update(account_id=None, used=None, network=None, key_id=None, depth=None, change=None, limit=20)
        logger.info("Wallet scan completed")
        logger.info("TXs")
        logger.info(txs)
    return server_wallet

def create_named_payment_address(wallet, address_name):
    """
    Creates new key/address with unique_name or
        params
            wallet object
            address name
        returns
            key_id of address associated to address name
            wallet object
            key id of for new address
    """
    key_id_named_addresses = [(x.name, x.id) for x in wallet.keys()]

    if address_name in [x[0] for x in key_id_named_addresses]:
        key_id = [
            key_id for (name, key_id) in key_id_named_addresses if address_name == name
        ][0]
        logger.info(f"named address: {address_name} already exists\nID: {key_id}")
        return key_id, wallet
    else:
        k = wallet.new_key(name=address_name)
        key_id = k.key_id
        return key_id, wallet


def sweep_wallet(trg_address, all_keys=False):
    '''
    Sweeping wallet extract all coins to target address
    '''
    # load wallet and update unspent transactions
    src_wallet=get_wallet(scan=True)

    amount_btc = Decimal(0.0) 
    no_keys = 0 
    tx_str = ""

    if not all_keys:
        logger.info("Sweeping keys for which billing status true, shipped true and transferred false")
        orders = Order.objects.filter(billing_status=True, shipped=True, transferred=False)
        if len(orders) > 0: 
            logger.info(f"Number of orders that met conditions: {len(orders)}")
            input_key_ids = []
            for order in orders:
                order_key = order.order_key
                key_id_named_addresses = dict(
                    [(x.name, x.id) for x in src_wallet.keys() if x.name == order_key]
                )
                kid = key_id_named_addresses[order_key]
                input_key_ids.append(kid)
        else:
            logger.info("No completed orders that have not yet been transferred. No sweep completed")
            return amount_btc, no_keys, tx_str
    else:
        logger.info("Transfering funds from ALL keys")
        input_key_ids = None


    if src_wallet.balance() > 0.0:
        logger.info(f"Balance of {src_wallet.balance()} found")
        logger.info("Sweeping ... ")
        logger.info(f"Will the transcations be made offline? - {settings.PAYMENT_OFFLINE}")
        txs = src_wallet.sweep(trg_address,
                            network=settings.PAYMENT_NETWORK,
                            max_utxos=999,
                            min_confirms=1,
                            input_key_id=input_key_ids, 
                            locktime=0,
                            offline=settings.PAYMENT_OFFLINE,)
        logger.info("Finished sweeping")
        logger.info("Transaction info:")
        logger.info(txs.info())
        
        satoshis  = src_wallet.balance()
        amount_btc = Decimal(int(satoshis) * 10e-9)
        try: 
            no_keys = len(input_key_ids)
        except TypeError:
            # if input_ids = None, I am scanned my entire wallet. 
            no_keys = len(txs.inputs)

        tx_str = str(txs)

    # Only update transferred status when were not sweeping the entire wallet.
    if not all_keys:
        # if there have been transferred orders.
        if len(orders)>0:
            logger.info("Swept wallet and updating orders")
            for order in orders:
                order.transferred = True 
                order.save()
                
    return amount_btc, no_keys, tx_str