from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # what will the admin see in the admin panel when viewing a list of the cateogry the DB
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "title",
        "created_by",
        "slug",
        "price",
        "in_stock",
        "created",
        "updated",
    ]

    list_filter = ["in_stock", "is_active"]
    list_editable = ["price", "in_stock"]

    prepopulated_fields = {"slug": ("title",)}
