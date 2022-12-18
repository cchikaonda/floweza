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

@login_required
def order_list(request):
    orders = Order.objects.filter(customer = request.user)
    zero_balance = Money(0.0, 'MWK')
    context = {
        'orders':orders,
        'title':'Orders',
        'zero_balance':zero_balance,
    }
    return render(request, 'orders_list.html', context=context)


@login_required
def edit_order(request, id):
    order = get_object_or_404(Order, id = id)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    context = {
        'form':form,
        'order':order,
        }
    return render(request, 'edit_order.html', context=context)

@login_required
def add_payment(request, id):
    order = get_object_or_404(Order, id = id)
    form = AddPaymentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            paid_amount = form.cleaned_data.get('paid_amount')
            payment_mode = request.POST.get('payment_mode')
            reference = request.POST.get('reference')
            payment = Payment()
            payment.payment_mode = payment_mode
            payment.paid_amount = paid_amount
            payment.reference = reference
            
            payment.order_id = order.code
            payment.save()
            order.payments.add(payment)
            order.save()
            messages.success(request, "Payment Successfully made!")
            return redirect('order_list')
    context = {
        'form':form,
        'order':order,
        }
    return render(request, 'add_payment.html', context=context)