from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

from basket.basket import Basket
from account.models import UserBase
from orders.models import Order, OrderItem

from review.models import Review, ProductReview
from store.models import Product
import logging 
from .forms import ReviewForm
from django.http import HttpResponse


logger = logging.getLogger("django")


import json 
import copy
@login_required
def add_review(request):
    if request.method == "POST":
        data  = copy.deepcopy(request.POST)
        data['orderId'] = int(data['orderId'])
        data['rate'] = int(data['rate'])
        review_form = ReviewForm(data)
        if review_form.is_valid(): 
            print(review_form.cleaned_data) 
            d = review_form.cleaned_data
            order_id = d['orderId']
            del d["orderId"]
            order = Order.objects.get(pk=order_id)
            da = {"order":order, **d}
            review = Review(**da)
            review.save()
            order_items = OrderItem.objects.filter(order=order)
            for order_item in order_items:
                product = Product.objects.get(title=order_item.product)
                product_review = ProductReview(rate=da['rate'], comment=da['comment'],review=review, product=product)
                product_review.save()
            
            order.reviewed = True
            order.save()
        return redirect("account:dashboard")
    
    else:
        return HttpResponse()





