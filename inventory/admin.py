from django.contrib import admin
from django.contrib import admin
from django.contrib.auth import get_user_model
from django import forms
from .models import *

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_description')
    search_fields = ['category_name', ]

    class Meta:
        model = ItemCategory
admin.site.register(ItemCategory, ItemCategoryAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'item_name','price','discount_price',
        'category',
        'item_description', 'seller', 'active','image'
        )
    search_fields = ['item_name', ]
    class Meta:
        model = Item
admin.site.register(Item, ItemAdmin)