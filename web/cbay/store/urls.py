from django.urls import path

from . import views

# matches the /core/urls namespace url pattern list
app_name = "store"

urlpatterns = [
    path("", views.product_all, name="product_all"),
    path("<slug:item_slug>", views.product_detail, name="product_detail"),
    path("search/<slug:category_slug>/", views.category_list, name="category_list"),
]
