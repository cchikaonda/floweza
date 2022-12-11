
from django.contrib import admin
from django.contrib.auth import get_user_model
from django import forms

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from constance.admin import ConstanceAdmin, ConstanceForm, Config

from order.models import OrderItem, Order, Payment

# Register your models here.
CustomUser = get_user_model()

admin.site.register(OrderItem)

admin.site.register(Order)

admin.site.register(Payment)