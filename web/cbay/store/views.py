from django.shortcuts import get_object_or_404, render

from .models import Category, Product
from review.models import ProductReview
from django.db.models import Avg
from django.core.paginator import Paginator

def product_all(request):
    products = Product.products.all()
    return render(request, "store/home.html", {"products": products})


def product_detail(request, item_slug):
    """Getting single product details"""
    product = get_object_or_404(Product, slug=item_slug, in_stock=True, is_active=True)
    reviews = ProductReview.objects.filter(product=product).order_by('-created')
    avg_rate = list(reviews.aggregate(Avg("rate")).values())[0]
    review_pages = Paginator(reviews, 5)
    page_number = request.GET.get("page")
    page_obj = review_pages.get_page(page_number)
     
    return render(request, "store/products/single.html", {"product": product, "reviews": reviews, "review_pages":page_obj,  "avg_rate": avg_rate, "no_review": len(reviews)})


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(
        request,
        "store/products/category.html",
        {"category": category, "products": products},
    )
