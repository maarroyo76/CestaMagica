from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/<int:id>/', views.vista_producto, name='vista_producto'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/<int:id>/', views.vista_categoria, name='vista_categoria'),
    path('marcas/', views.lista_marcas, name='lista_marcas'),
    path('marcas/<int:id>/', views.vista_marca, name='vista_marca'),
]