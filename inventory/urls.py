from mainapp.views import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('inventory/', inventory_dashboard, name = 'inventory_dashboard'), 
]