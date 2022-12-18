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
    context = {
        'orders':orders,
        'title':'Orders',
    }
    return render(request, 'orders_list.html', context=context)