from decimal import Decimal
from django.conf import settings
from django.db import models

from store.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order_user"
    )
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=50, default="")
    address1 = models.CharField(max_length=250, default="")
    city = models.CharField(max_length=100, default="")
    post_code = models.CharField(max_length=20, default="")
    county = models.CharField(max_length=20, default="")
    country = models.CharField(max_length=20, default="")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    transferred = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return str(self.created)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
