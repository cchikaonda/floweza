from django import template
from mainapp.models import *
from inventory.models import *

register = template.Library()

@register.filter
def user_count(user):
    if user.is_authenticated:
        qs = CustomUser.objects.all().count()
    return qs

@register.filter
def item_category_count(user):
    qs = ItemCategory.objects.all().count()
    return qs

@register.filter
def items_count(user):
    qs = Item.objects.all().count()
    return qs



@register.filter
def customers_count(user):
    qs = CustomUser.objects.filter(user_role = "Customer").count()
    return qs

