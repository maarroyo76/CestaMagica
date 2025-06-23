from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:producto_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:producto_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('decrement/<int:producto_id>/', views.decrement_in_cart, name='decrement_in_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('', views.cart_detail, name='cart_detail'),
    path('get_cart_state/', views.get_cart_state, name='get_cart_state'),
    path('update_quantity/<int:producto_id>/', views.update_quantity, name='update_quantity'),
]
