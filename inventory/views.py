from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render,redirect, get_object_or_404
import expenses
from inventory.models import ItemCategory, Unit, Item, Stock, Supplier
from pos.models import Customer,OrderItem, Order
from expenses.models import Expense, ExpenseCategory
from inventory.forms import *
from pos.forms import *
from django.template.loader import render_to_string

from constance import config
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.db.models import AutoField,IntegerField,FloatField,ExpressionWrapper, F, DecimalField, Count, Sum
from djmoney.money import Money
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import date, timedelta, datetime
from django.db.models.functions import Lower
from djmoney.models.fields import MoneyField
from inventory.forms import *



# Create your views here.
@login_required
def inventory_dashboard(request):
    context = {

    }
    return render(request, 'inventory_dashboard.html', context)

