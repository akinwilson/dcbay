from django.contrib.auth.models import User
from account.models import UserBase
from django.db import models
from django.urls import reverse


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)  # category name
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:

        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(
        Category, related_name="product", on_delete=models.CASCADE
    )
    # **User** is a standard django table
    created_by = models.ForeignKey(
        UserBase, on_delete=models.CASCADE, related_name="product_creator"
    )
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, default="")
    uses = models.TextField(blank=True)
    dosage = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    # WE ARE NOT STORING IMAGE IN DB ---> WE STORE LINK TO IT
    image = models.ImageField(upload_to="images/", default="images/default.png")
    slug = models.SlugField(max_length=255, unique=True)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = "Products"
        ordering = ("-created",)

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def __str__(self):
        return self.title
