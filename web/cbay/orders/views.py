from django.http.response import JsonResponse


from basket.basket import Basket
from .forms import OrderForm
from .models import Order, OrderItem
import uuid

from django.views.decorators.csrf import ensure_csrf_cookie
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
import logging
from django.shortcuts import redirect

logger = logging.getLogger("django")


def add(request):
    basket = Basket(request)
    if request.method == "POST": 
        order_form = OrderForm(request.POST)
        data = order_form.data
        if order_form.is_valid():
            # Create order if valid data. 
            # Check if order exists
            if Order.objects.filter(order_key= data.get("order_key")).exists():
                logger.info("Order DID exist in table")
                logger.info(f"Order key: { data.get('order_key')}")
                pass
            else:
                logger.info("Order did NOT exist in table")
                logger.info(f"Order key: { data.get('order_key')}")

                order = Order.objects.create(
                    user_id=request.user.id,
                    first_name=data.get("first_name"),
                    last_name=data.get("last_name"),
                    address1=data.get("address"),
                    city=data.get("city"),
                    country=data.get("country"),
                    county=data.get("county"),
                    email=data.get("email"),
                    post_code=data.get("post_code"),
                    total_paid=basket.get_total_price_with_shipping(),
                    order_key= data.get("order_key"),
                )
                order_id = order.pk

                for item in basket:
                    OrderItem.objects.create(
                        order_id=order_id,
                        product=item["product"],
                        price=item["price"],
                        quantity=item["quantity"],
                    )
            return  redirect("payment:order_placed") 
        else:
            # form not valid condition
            context = {
                "form": OrderForm(initial={"order_key":str(uuid.uuid4())}),
                }

            return render(request, "payment/home.html", context=context)
    else:
        response = JsonResponse({"msg": "Get reuqest made"})
        return response

def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
