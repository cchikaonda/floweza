from django.shortcuts import render,redirect, get_object_or_404
from mainapp.models import *
from django.contrib import messages
from constance import config
from django.utils import timezone
from datetime import date, timedelta, datetime
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.core import serializers
import json
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from floweza import settings
import time
from djmoney.money import Money
from django.template.loader import render_to_string
from inventory.models import ItemCategory, Item


from django.http import HttpResponse
from basket.basket import Basket
from order.forms import *
from order.models import *
from inventory.forms import *



@login_required
def logout_request(request):
    logout(request)
    response = redirect('logout')
    if 'user_loggedin' in request.session:
        del request.session['opened_order']
    messages.success(request, "Successfully logged out!")
    return redirect('index')

def index(request):
    item_search_form = ItemSearchForm()
    item_categories = ItemCategory.objects.all()
    query = request.POST.get("item_name", None)
    items = Item.objects.filter(active = True)
    items_count = items.count()

    if query is not None:
        items = (items.filter(item_name__startswith  = query))|items.filter(item_name__icontains = query)
        items_count = items.count()
        
    context = {
        'item_search_form':item_search_form,
        'items':items,
        'items_count':items_count,
        'item_categories':item_categories,
        'title':'Floweza MIS',
    }
    return render(request, 'index.html', context=context)

def shop(request):
    item_search_form = ItemSearchForm()
    item_categories = ItemCategory.objects.all()
    query = request.POST.get("item_name", None)
    items = Item.objects.filter(active = True)
    items_count = items.count()

    if query is not None:
        items = (items.filter(item_name__startswith  = query))|items.filter(item_name__icontains = query)
        items_count = items.count()
        
    context = {
        'items':items,
        'items_count':items_count,
        'item_categories':item_categories,
        'title':'Floweza MIS',
        'header':'Shop',
        'item_search_form':item_search_form,
    }
    return render(request, 'shop.html', context)

def shopping_cart(request):
    item_categories = ItemCategory.objects.all()
    basket = Basket(request)
    deliveryoptions = DeliveryOptions.objects.all()
    delivery_cost = str(basket.get_delivery_price())
    
    context = {
        'title':'Floweza MIS',
        'header':'Shopping Cart',
        'basket':basket,
        'deliveryoptions':deliveryoptions,
        'delivery_cost':delivery_cost,
        'item_categories':item_categories,
    }
    return render(request, 'shopping_cart.html', context)

def checkout(request):
    payment_form = AddPaymentForm(request.POST or None)
    basket = Basket(request)
    address_form = UserAddressForm()
    total_price = str(basket.get_total_price())
    addresses = ''
    address = ''
    # paid_amount = payment_form.cleaned_data.get('paid_amount')
    if request.user.is_authenticated:
        addresses_check = Address.objects.filter(customer=request.user)
        if addresses_check.exists():
            address = Address.objects.get(customer=request.user, default = True)
            addresses = Address.objects.filter(customer=request.user, default = False)
    
    if request.method == "POST":
        if payment_form.is_valid():
            paid_amount = payment_form.cleaned_data.get('paid_amount')
            payment_mode = request.POST.get('payment_mode')
            reference = request.POST.get('reference')

            order_total_cost =  basket.get_total_price()

            session = request.session
            delivery_id = session["purchase"]["delivery_id"]
            delivery_option = DeliveryOptions.objects.get(id = delivery_id)
            
            order = Order.objects.create(customer = request.user, address = address, order_total_cost = order_total_cost, delivery_option = delivery_option)
            order.code = order.get_code()
            order.save()
            code = order.get_code()

            
            
            for item in basket:
                
                ordered_item = OrderItem.objects.create(
                    order_id=code, item =item["item"], ordered_item_price=item["price"], quantity=item["qty"]
                )
                order.items.add(ordered_item)
                order.save()

            payment = Payment()
            payment.payment_mode = payment_mode
            payment.paid_amount = paid_amount
            payment.reference = reference
            
            payment.order_id = code
            payment.save()
            order.payments.add(payment)
            order.save()
            messages.success(request, "Order Successfully placed!")
            del request.session['basket']
            del request.session['purchase']
            return redirect('index')

    context = {
        'title':'Floweza MIS',
        'header': 'Checkout',
        'basket':basket,
        'address':address,
        'addresses':addresses,
        'address_form':address_form,
        'total_price':total_price,
        'payment_form':payment_form,
    }
    return render(request, 'checkout.html', context)

def item_details(request, id):
    item = get_object_or_404(Item, id = id)
    context = {
        'item':item,
        'title':'Floweza MIS',
        'header': 'Item details',
    }
    return render(request, 'item_details.html', context)

def category_list(request):
    categories = ItemCategory.objects.all()
    context = {
        'categories':categories,
        'title':'Floweza MIS',
        'header': 'Item Category List',
        
    }
    return render(request, 'admin/item_categories/category_list.html', context)

@login_required
def category_create(request):
    if request.method == 'POST':
        form = AddItemCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = AddItemCategoryForm()
    return render(request, 'admin/item_categories/category_create.html', {'form':form,})

@login_required
def category_update(request, id):
    category = get_object_or_404(ItemCategory, id=id)
    form = AddItemCategoryForm(instance=category)
    if request.method == 'POST':
        form = AddItemCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = AddItemCategoryForm(instance=category)
    return render(request, 'admin/item_categories/category_update.html', {'form':form,},)

def item_list(request):
    items = Item.objects.filter(seller = request.user)
    context = {
        'items':items,
        'title':'Floweza MIS',
        'header': 'Item List',
        
    }
    return render(request, 'admin/items/items_list.html', context)

@login_required
def item_create(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = AddItemForm()
    return render(request, 'admin/items/item_create.html', {'form':form,})

@login_required
def item_update(request, id):
    product = get_object_or_404(Item, id=id)
    form = AddItemForm(instance=product)
    if request.method == 'POST':
        form = AddItemForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = AddItemForm(instance=product)
    return render(request, 'admin/items/item_update.html', {'form':form,},)


def contact(request):
    item_categories = ItemCategory.objects.all()
    items = Item.objects.all()
    context = {
        'items':items,
        'item_categories':item_categories,
        'title':'Floweza MIS',
        'header': 'Contact',
    }
    return render(request, 'contact.html', context)


@login_required
def addresses(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "addresses.html", {"addresses": addresses})

@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("addresses"))
        else:
            return HttpResponse("Error handler content", status=400)
    else:
        address_form = UserAddressForm()
    return render(request, "edit_addresses.html", {"form": address_form})

@login_required
def add_address_from_checkout(request):
    address_form = UserAddressForm(data=request.POST)
    if request.method == "POST":
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            Address.objects.filter(customer=request.user).update(default=True)
            messages.success(request, "Address Successfully Created!")
            return HttpResponseRedirect(reverse("checkout"))
        else:
            return HttpResponse("Error handler content", status=400)


@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)

    previous_url = request.META.get("HTTP_REFERER")

    if "delivery_address" in previous_url:
        return redirect("delivery_address")

    return redirect("addresses")

@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "edit_addresses.html", {"form": address_form})

@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "delivery_choices.html", {"deliveryoptions": deliveryoptions})


@login_required(login_url="/login/")
def pages(request):
    user = request.user
    context = {}
    return render(request, 'admin/home_admin.html', context=context)
