from django.contrib import admin
from django.contrib.auth import get_user_model
from django import forms

from django.contrib.auth.models import Group

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import *
from constance.admin import ConstanceAdmin, ConstanceForm, Config

from mainapp.models import *
from mainapp.forms import GroupAdminForm


class CustomConfigForm(ConstanceForm):
      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

User = get_user_model()

class CustomUserAdmin(BaseUserAdmin):
    #the forms to add and change user instances
    add_form = UserAdminCreationForm
    list_display = ('full_name','email','user_role', 'admin','seller','active','transporter','customer','phone_number', 'image','password',)
    list_filter = ('seller','admin','active','transporter','customer','groups')
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal information', {'fields': ('full_name','phone_number','image')}),
        ('Permissions', {'fields': ('seller','admin', 'user_role','active','transporter','customer','password','groups')}),
    )
    #add_fieldsets is not a standard ModelAdmin attribute. UserAdmins
    #overrides get_fieldsets to use this attribute when creating a user
    add_fieldsets = (
        (None,{
             'classes': ('wide',),
             'fields': ('email','full_name','phone_number','image','user_role','admin','active','seller','transporter','customer','groups','password1', 'password2'),}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)

# Unregister the original Group admin.
admin.site.unregister(Group)

admin.site.register(Address)
admin.site.register(DeliveryOptions)






