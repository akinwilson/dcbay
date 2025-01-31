# Generated by Django 4.1.3 on 2022-11-17 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
            ],
            options={
                "verbose_name_plural": "categories",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("subtitle", models.CharField(default="", max_length=255)),
                ("uses", models.TextField(blank=True)),
                ("dosage", models.TextField(blank=True)),
                ("side_effects", models.TextField(blank=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=4)),
                (
                    "image",
                    models.ImageField(
                        default="images/default.png", upload_to="images/"
                    ),
                ),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("in_stock", models.BooleanField(default=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product",
                        to="store.category",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_creator",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Products",
                "ordering": ("-created",),
            },
        ),
    ]
