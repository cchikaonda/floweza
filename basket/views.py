from django.shortcuts import render, redirect, get_object_or_404
from .basket import Basket
from inventory.models import Item
from mainapp.models import DeliveryOptions
from .forms import BasketAddProductForm
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
from djmoney.money import Money


# Create your views here.

# @require_POST
def basket_add(request, item_id):
    basket = Basket(request)
    item = get_object_or_404(Item, id = item_id)
    if request.method == "POST":
        qty = int(request.POST.get('qty'))
        basket.add(item = item, qty = qty, override_qty='override')
    return redirect ('shopping_cart')

def basket_remove(request, item_id):
    basket = Basket(request)
    item = get_object_or_404(Item, id = item_id)
    basket.delete(item.id)
    return redirect ('shopping_cart')

def basket_detail(request):
    basket = Basket(request)
    return render(request, 'basket/detail.html', {'basket':basket})

def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)

        updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price.amount)
        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True
            
        response = JsonResponse({"total": str(updated_total_price), "delivery_price": str(delivery_type.delivery_price)})
        return response

