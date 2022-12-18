from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from mainapp.views import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # The home page
    path('', index, name='index'),
    path('logout/', auth_views.LoginView.as_view(), name = 'logout'),
    path('logout_request', logout_request, name = 'logout_request'),

    # Matches any html file
    re_path('pages', pages, name='pages'),
    path('shop', shop, name = 'shop'),
    path('shopping_cart', shopping_cart, name = 'shopping_cart'),
    path('checkout', checkout, name = 'checkout'),
    path('item_details/<int:id>/', item_details, name = 'item_details'),
    path('contact', contact, name = 'contact'),
    path('addresses', addresses, name = 'addresses'),
    path("addresses/set_default/<slug:id>/", set_default, name="set_default"),
    path("add_address/", add_address, name="add_address"),
    path("addresses/edit/<slug:id>/", edit_address, name="edit_address"),
    path("deliverychoices", deliverychoices, name="deliverychoices"),

    path("add_address_from_checkout", add_address_from_checkout, name="add_address_from_checkout"),


    
    
    
    
]