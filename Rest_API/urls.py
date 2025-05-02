from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/<id>', views.vista_producto, name='vista_producto'),
    path('categorias/', views.lista_productos, name='lista_productos'),
    path('categorias/<id>', views.vista_producto, name='vista_producto'),
    path('marcas/', views.lista_productos, name='lista_productos'),
    path('marcas/<id>', views.vista_producto, name='vista_producto'),
]