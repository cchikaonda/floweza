from django.db import models
from django.conf import settings
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.shortcuts import reverse
from constance import config

from pymysql import NULL

from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import date, timedelta, datetime, time


class ItemCategory(models.Model):
    category_name = models.CharField(max_length=50)
    category_description = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    
    @staticmethod
    def get_all_item_categories():
        return ItemCategory.objects.all()

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_description = models.TextField()
    image = models.ImageField(default="ecom_product6_b.png", upload_to='items/', null=True, blank=True)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='MWK')
    discount_price = MoneyField(max_digits=14, null=True, blank=True, decimal_places=2, default_currency='MWK')
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    quantity_at_hand = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.item_name
    
    @staticmethod
    def get_all_items():
        return Item.objects.all().order_by('item_name')

    @staticmethod
    def get_all_items_by_category_id(category_id):
        if category_id:
            return Item.objects.filter(category=category_id).order_by('item_name')
        else:
            return Item.get_all_items()
    
    def selling_price(self):
        if self.discount_price:
            return self.discount_price
        else:
            return self.price





    









