from pickle import FALSE
from django.db import models
from django.conf import settings
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.shortcuts import reverse
from constance import config
from datetime import date

from djmoney.money import Money
from mainapp.models import CustomUser
from inventory.models import Item
from django.db.models.functions import Abs
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class OrderItem(models.Model):
    order_id = models.CharField(default="", max_length=30)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete = models.SET_NULL, null = True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)
    ordered_item_price = MoneyField(max_digits=14, decimal_places=2, default_currency='MWK', default= 0.0)
    ordered_items_total = MoneyField(max_digits=14, decimal_places=2, default_currency='MWK', default= 0.0)
    ordered_time = models.DateTimeField(auto_now_add=True, null = True)

    @property
    def price(self):
        return self.item.selling_price()
    

    @property
    def amount(self):
        amount = MoneyField()
        amount = self.quantity * self.item.selling_price()
        return amount

    @property
    def get_total_amount(self):
        return self.amount
    
    def get_item_discount(self):
        if self.item.discount_price:
            return self.quantity * self.item.price - self.quantity * self.item.discount_price
        else:
            return 0

    def __str__(self):
        return f"{self.quantity} {self.item.unit} of {self.item.item_name}"
    
    @property
    def get_ordered_item_category(self):
        return self.item.category
    
    def check_if_ordered_item_is_in_refund_order(self):
        refund_order_item = RefundOrderItem.objects.get(order_id = self.order_id)  
        if refund_order_item != None:
            return True
        else:
            return False

@receiver(post_save, sender=OrderItem)
def update_orderitem_quantities(sender, instance, **kwargs):
    OrderItem.objects.filter(id=instance.id).update(ordered_item_price=instance.price, ordered_items_total = instance.amount)

class Payment(models.Model):
    payment_options =(
        ('Cash','Cash'),
        ('Mpamba', 'Mpamba'),
        ('Airtel Money', 'Airtel Money'),
        ('Bank', 'Bank'),
        
    )
    customer = models.ForeignKey(CustomUser, on_delete = models.SET_NULL, null = True)
    payment_mode = models.CharField(max_length = 15, choices = payment_options, default='Cash')
    order_id = models.CharField(max_length=20, null=True)
    order_type = models.CharField(max_length=20, null=True)
    paid_amount = MoneyField(max_digits=14, decimal_places=2, default_currency='MWK', default= 0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}'.format(self.paid_amount)

order_status_options =(
        ('Pending','Pending'),
        ('Awaiting Delivery', 'Awaiting Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        
    )
class Order(models.Model):
    def gen_code(self):
            return 'ORD%04d'%self.pk
    code = models.CharField(max_length=50, null=True, default="0000")
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(OrderItem)
    order_status = models.CharField(max_length = 20, choices = order_status_options, default='Pending')
    payments = models.ManyToManyField(Payment)
    order_total_cost = MoneyField(max_digits=14, decimal_places=2, default_currency='MWK', default= 0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_reference = models.CharField(max_length=50, null=True)

  
    def __str__(self):
        return '{1} {0}'.format(self.created_at, self.customer)

    @property
    def get_code(self):
        return self.gen_code
    
    
    
    def order_total(self):
        total = Money('0.0', 'MWK')
        for order_item in self.items.all():
            total += order_item.amount
        return total 
    
    def all_items_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.amount
        return total

    def get_total_discount(self):
        discount_total = 0
        for ordered_item in self.items.all():
            discount_total += ordered_item.get_item_discount()
        return discount_total
    

    
    def total_paid_amount(self):
        sum_paid = Money(0.0, 'MWK')
        for payment in self.payments.all():
            sum_paid += payment.paid_amount
        return sum_paid


    
    def get_balance(self):
        balance = Money(0.0, 'MWK')
        sum_paid = self.total_paid_amount()
        if sum_paid < self.order_total_due():
            return self.order_total_due() - sum_paid
        else:
            return balance
    
    def default_amount_paid(self):
        default_money = Money(0.0, 'MWK')
        return default_money 

    @property
    def get_customer(self):
        return self.items.customer
    

