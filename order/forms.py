from dataclasses import field
from django import forms
from django.contrib.auth import get_user_model
from mainapp.models import CustomUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.views.generic import UpdateView
from django.db import models
from django_countries.fields import CountryField
# from constance.admin import ConstanceAdmin, ConstanceForm, Config
from djmoney.forms.widgets import MoneyWidget
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Payment, Order
from inventory.models import Item
from django.core.validators import RegexValidator



class CustomMoneyWidget(MoneyWidget):
    def format_output(self, rendered_widgets):
        return ('<div class="row form-group">'
                    '<div class="col-sm-12 ">%s</div>'
                    '<div class="col-sm-12 ">%s</div>'
                '</div>') % tuple(rendered_widgets)

class AddPaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddPaymentForm, self).__init__(*args, **kwargs)
        paid_amount, currency = self.fields['paid_amount'].fields
        self.fields['paid_amount'].widget = CustomMoneyWidget(amount_widget = paid_amount.widget, currency_widget = currency.widget)
    class Meta:
        model = Payment
        fields = ('payment_mode','paid_amount','reference')
        widgets = {
                'paid_amount': forms.TextInput(attrs={'class': 'form-control pos_form',}),
                'payment_mode': forms.Select(attrs={'class': 'form-control pos_form',}),
                'paid_amount': forms.TextInput(attrs={'class': 'form-control pos_form',}),
        }
