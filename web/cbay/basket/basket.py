from store.models import Product
from decimal import Decimal
from django.http import JsonResponse
import copy
from django.conf import settings


class Basket:

    """
    A base basket class providing befault behaviour that can be inherted or overrided
    """

    def __init__(
        self,
        request,
    ):

        self.session = request.session
        # session key
        basket = self.session.get("skey")

        if "skey" not in request.session:
            # setting key value of skey to equal empty dict and basket
            basket = self.session["skey"] = {}

        self.basket = basket

    def save(self):
        self.session.modified = True

    def add(self, product, product_qty):

        product_id = product.id

        if product_id not in self.basket:

            self.basket[product_id] = {
                "price": str(product.price),
                "quantity": int(product_qty),
            }

        # will modify the DB via true flag
        self.save()
        return JsonResponse({"Success": True})

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]["product"] = product
        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        basket_len = sum(item["quantity"] for item in self.basket.values())

        return 0 if basket_len is None else basket_len

    def get_total_price(self):
        return sum(
            item["quantity"] * Decimal(item["price"]) for item in self.basket.values()
        )

    def get_total_price_with_shipping(self):
        return sum(item["quantity"] * Decimal(item["price"]) for item in self.basket.values())  + Decimal(settings.SHIPPING_COST) 
    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

        return JsonResponse({"Success": True})

    def update(self, product, qty):
        """
        Update values in session data
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]["quantity"] = qty
        self.save()

        return JsonResponse({"Success": True})

    def clear(self):
        """
        Delete basket
        """

        basket = copy.deepcopy(self.basket)

        for product_id in basket:
            del self.basket[product_id]

        self.save()
        return JsonResponse({"Success": True})
