from django.db import models
from django.conf import settings
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.shortcuts import reverse
from constance import config
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import Group

from django.utils.translation import gettext_lazy as _
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, full_name = None ,user_role = None,phone_number = None,password = None, is_staff = True, is_active = True, is_seller = True, is_admin = False, is_customer = False, is_transporter = False):
        if not email:
            raise ValueError ("Users must have an email address")
        if not password:
            raise ValueError ("Users must have a password")
        if not full_name:
            raise ValueError (" Users must have a password")

        user_obj = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
            phone_number = phone_number,
            user_role = user_role,
        )
        user_obj.set_password(password) # change user password
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.seller = is_seller
        user_obj.transporter = is_transporter
        user_obj.customer = is_customer
        user_obj.staff = is_staff
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email,full_name = None,phone_number =None, password = None, user_role = None):
        user = self.create_user(
                email,
                full_name,
                phone_number,
                password = password,
                is_admin=True,
                is_active = True,
                is_seller = True,
                is_staff = True,
                is_transporter = True,
                is_customer = True,
        )
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank = True, null=True)
    roles =(
        ('Admin','Admin'),
        ('Seller', 'Seller'),
        ('Transporter', 'Transporter'),
        ('Customer', 'Customer'),
    )
    user_role = models.CharField(max_length = 15, choices = roles, default = "Customer")
    phone_number = PhoneNumberField(null = True, blank = True)
    username = None
    staff = models.BooleanField(default=True) #can login
    active = models.BooleanField(default=True) #can login
    admin = models.BooleanField(default=False) # Adminstrator
    seller = models.BooleanField(default=False) #seller
    customer = models.BooleanField(default=False)
    transporter = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default = "avatar0.jpg", null = True, blank = True)
    group = Group.add_to_class('description', models.CharField(max_length=180,null=True, blank=True))
    USERNAME_FIELD = 'email' #loginuser
    REQUIRED_FIELDS = ['full_name','phone_number',]


    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_seller(self):
        return self.seller
    
    @property
    def is_customer(self):
        return self.seller

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active
    
    @property
    def is_transporter(self):
        return self.transporter
    
    
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Address(models.Model):
    """
    Address
    """
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    phone_number = PhoneNumberField(null = True, blank = True)
    area = models.CharField(max_length=50)
    district = models.CharField(max_length=150)
    physical_address = models.CharField(max_length=255)
    delivery_instructions = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return "{} Address".format(self.customer.full_name)


class DeliveryOptions(models.Model):
    """
    The Delivery methods table contining all delivery
    """

    DELIVERY_CHOICES = [
        ("IS", "In Store"),
        ("HD", "Home Delivery"),
        ("DD", "Digital Delivery"),
    ]

    delivery_name = models.CharField(
        verbose_name=_("delivery_name"),
        help_text=_("Required"),
        max_length=255,
    )
    delivery_price = MoneyField(
        decimal_places=2, 
        default_currency='MWK',
        verbose_name=_("delivery price"),
        help_text=_("Maximum 50 000"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 50 0000."),
            },
        },
        max_digits=14,
    )
    delivery_method = models.CharField(
        choices=DELIVERY_CHOICES,
        verbose_name=_("delivery_method"),
        help_text=_("Required"),
        max_length=255,
    )
    delivery_timeframe = models.CharField(
        verbose_name=_("delivery timeframe"),
        help_text=_("Required"),
        max_length=255,
    )
    delivery_window = models.CharField(
        verbose_name=_("delivery window"),
        help_text=_("Required"),
        max_length=255,
    )
    order = models.IntegerField(verbose_name=_("list order"), help_text=_("Required"), default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Delivery Option")
        verbose_name_plural = _("Delivery Options")

    def __str__(self):
        return self.delivery_name



    

