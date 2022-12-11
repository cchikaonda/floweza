from django.urls import path

from  basket.views import basket_add, basket_remove, basket_update_delivery
app_name = 'basket'

urlpatterns = [
    # path('', basket_detail, name='basket_detail'),
    path('add/<int:item_id>/', basket_add, name='basket_add'),
    path('remove/<int:item_id>/', basket_remove, name='basket_remove'),
    path("basket_update_delivery/", basket_update_delivery, name="basket_update_delivery"),
    # path('update/', views.basket_update, name='basket_update'),
]
