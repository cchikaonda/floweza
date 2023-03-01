from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from reports.views import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('reports_dashboard', reports_dashboard, name='reports_dashboard'),
    path('sales_report', sales_report, name='sales_report'),
]

