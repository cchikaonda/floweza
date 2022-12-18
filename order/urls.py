from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from order.views import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # The home page
    path('order_list', order_list, name='order_list'),
]