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



@login_required
def logout_request(request):
    logout(request)
    response = redirect('logout')
    if 'user_loggedin' in request.session:
        del request.session['opened_order']
    messages.success(request, "Successfully logged out!")
    return redirect('index')

def index(request):
    item_categories = ItemCategory.objects.all()
    items = Item.objects.all()
    context = {
        'items':items,
        'item_categories':item_categories,
        'title':'Floweza MIS',
    }
    return render(request, 'index.html', context=context)

def shop(request):
    item_categories = ItemCategory.objects.all()
    items = Item.objects.all()
    context = {
        'items':items,
        'item_categories':item_categories,
        'title':'Floweza MIS',
        'header':'Shop',
    }
    return render(request, 'shop.html', context)

def shopping_cart(request):
    basket = Basket(request)
    deliveryoptions = DeliveryOptions.objects.all()
    context = {
        'title':'Floweza MIS',
        'header':'Shopping Cart',
        'basket':basket,
        'deliveryoptions':deliveryoptions,
    }
    return render(request, 'shopping_cart.html', context)

def checkout(request):
    basket = Basket(request)
    address_form = UserAddressForm()
    
    context = {
        'title':'Floweza MIS',
        'header': 'Checkout',
        'basket':basket,
        'address_form':address_form,
        
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
    if user.user_role == 'Admin':
        if 'user_loggedin' in request.session:
            return render(request, 'admin/home_admin.html', context=context)
        else:
            messages.success(request, "Successfully logged in as Admin")
            request.session['user_loggedin'] = user.user_role
            return render(request, 'admin/home_admin.html', context=context)
    elif user.user_role == 'Seller':
        if request.COOKIES.get('user_loggedin') == None:
            request.COOKIES.set('user_loggedin')
            messages.success(request, "Successfully logged in as Seller")
        return render(request, 'seller/home_seller.html', context=context)
    elif user.user_role == 'Transporter':
        if request.COOKIES.get('user_loggedin') == None:
            request.COOKIES.set('user_loggedin')
            messages.success(request, "Successfully logged in as Transporter")
        return render(request, 'transporter/home_transporter.html', context=context)
    else:
        if request.COOKIES.get('user_loggedin') == None:
            request.COOKIES.set('user_loggedin')
            messages.success(request, "Successfully logged in as Customer")
        return render(request, 'customer/home_customer.html', context=context)
    # except TemplateDoesNotExist:
    #     html_template = loader.get_template('home/page-404.html')
    #     return HttpResponse(html_template.render(context, request))

    # except:
    #     html_template = loader.get_template('home/page-500.html')
    #     return HttpResponse(html_template.render(context, request))