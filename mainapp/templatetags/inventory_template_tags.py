from django import template
from mainapp.models import *
from inventory.models import *

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Quotation.objects.filter(user=user, ordered = False)
        if qs.exists():
            return qs[0].items.count()
    return 0
    
@register.filter
def user_count(user):
    if user.is_authenticated:
        qs = CustomUser.objects.all().count()
    return qs

@register.filter
def item_category_count(user):
    if user.is_authenticated:
        qs = ItemCategory.objects.all().count()
    return qs

@register.filter
def item_count(user):
    if user.is_authenticated:
        qs = Item.objects.all().count()
    return qs



@register.filter
def customers_count(user):
    if user.is_authenticated:
        qs = CustomUser.objects.filter(user_role = "Customer").count()
    return qs



@register.filter
def get_all_items_by_category_id(category_id):
    if category_id:
        return Expense.objects.filter(category=category_id).order_by('expense_name')
    else:
        return Expense.get_all_expense()
