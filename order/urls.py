from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from order.views import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('order_list', order_list, name='order_list'),
    path('edit_order/<int:id>/', edit_order, name='edit_order'),
    path('add_payment/<int:id>/', add_payment, name='add_payment'),
]