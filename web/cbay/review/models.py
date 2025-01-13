from django.db import models
from orders.models import Order
from store.models import Product
# Create your models here.

class Review(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    comment = models.TextField(default="",max_length=1024, null=True )
    rate = models.FloatField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.created: %B %d, %Y %H:%M:%S}'
    


class ProductReview(models.Model):
    review = models.ForeignKey(Review, related_name="review", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="product_review", on_delete=models.CASCADE)
    rate = models.FloatField(default=1)
    comment = models.TextField(default="",max_length=1024, null=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__ (self):
        return f"{self.product.title} | {self.review.created: %B %d, %Y %H:%M:%S}"