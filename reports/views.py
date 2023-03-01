from django.shortcuts import render
from order.models import *
from mainapp.models import *
from basket.models import *
from inventory.models import *
from authentication.models import *
from django.db.models import AutoField,IntegerField,FloatField,ExpressionWrapper, F, DecimalField, Count, Sum, Max
from reports.forms import SearchBetweenTwoDatesForm
from django.utils import timezone
from datetime import date, timedelta, datetime, time
# Create your views here.


def reports_dashboard(request):
    item_cats = ItemCategory.objects.all()
    user = request.user
    if user.is_admin == True:
        total_sales = Item.objects.all().values('category__category_name').annotate(total_quantity=Sum('orderitem__quantity')).annotate(sales_total = Sum('orderitem__ordered_items_total', output_field = FloatField() ))
        ordered_items = OrderItem.objects.all()
    else:
        total_sales = Item.objects.filter(seller = user).values('category__category_name').annotate(total_quantity=Sum('orderitem__quantity')).annotate(sales_total = Sum('orderitem__ordered_items_total', output_field = FloatField() ))
        ordered_items = OrderItem.objects.filter(item__seller = user)

    gross_sales = 0
    total_items_sold = 0

    for ordered_item in ordered_items:
        gross_sales += ordered_item.ordered_items_total
        total_items_sold += ordered_item.quantity
    
    context = {
        'header': 'Reports',
        'total_sales':total_sales,
        'gross_sales':gross_sales,
        'total_items_sold':total_items_sold,

    }
    return render(request, 'reports_dashboard.html', context)

def sales_report(request):
    form = SearchBetweenTwoDatesForm()
    item_cat = "All Categories"
    total_cost_items_ordered = Money('0.0', 'MWK')

    item_categories = ItemCategory.objects.all().order_by('category_name')

    ordered_items = all_days_sales(request, 0)

    if request.method == "POST":
        if form.is_valid:
            from_date = request.POST.get('start_date_time')
            to_date = request.POST.get('end_date_time')
        
            item_cat = request.POST.get('item_categories_option')

        
        if is_valid_queryparam(from_date) and is_valid_queryparam(to_date):
            category_id = item_cat
            get_item_cat = ItemCategory.objects.filter(category_name = category_id)
            if get_item_cat.exists():
                ordered_items = ordered_items.filter(ordered_time__gte = from_date, ordered_time__lte = to_date, item__category__in = get_item_cat)
            ordered_items = ordered_items.filter(ordered_time__gte = from_date, ordered_time__lte = to_date)

    sum_ordered_items_count = 0
    total_cost_items_ordered = Money(0.0, 'MWK') 
    for ordered_items_count in ordered_items:
        sum_ordered_items_count += ordered_items_count.quantity
        total_cost_items_ordered += ordered_items_count.ordered_items_total

    context = {
        'header': 'Sales Report',
        'form':form,
        'item_cat':item_cat,
        'ordered_items':ordered_items,
        'total_cost_items_ordered':total_cost_items_ordered,
        'item_categories':item_categories,
    }
    return render(request, 'sales_report.html', context)

def is_valid_report_default_report_period(param):
    return param != '' and param is not None and param != 0

def is_valid_item_category(param):
    return param != '' and param is not None and param != 0 and param != 1

def is_valid_queryparam(param):
    return param != '' and param is not None

def all_days_sales(request, category):
    user = request.user
    category_id = str(category)
    get_item_cat = ItemCategory.objects.filter(category_name = category_id)
    if get_item_cat.exists():
        if user.is_admin == True:
            return OrderItem.objects.filter(item__category__in = get_item_cat)
        else:
            return OrderItem.objects.filter(item__seller = user, item__category__in = get_item_cat)
    else:
        if user.is_admin == True:
            return OrderItem.objects.all()
        else:
            return OrderItem.objects.filter(item__seller = user)

