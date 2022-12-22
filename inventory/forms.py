from django import forms
from django.contrib.auth import get_user_model
from inventory.models import *
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.views.generic import UpdateView
from django.db import models
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import Group, User



class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('item_name','image','price','discount_price', 'category', 'item_description', 'active')
        widgets = {
                'item_description':forms.TextInput(attrs={'class': 'form-control',}),
                }


class AddItemCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        fields = ('category_name', 'category_description',)
        widgets = {
                'category_description':forms.TextInput(attrs={'class': 'form-control',}),
                }

    


