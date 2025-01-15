from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.productos, name='productos'),
    path('gestion/', views.gestion, name='gestion'),
    path('contacto/', views.contacto, name='contacto'),
    path('gestion/agregar/', views.agregar_producto, name='agregar_producto'),
    path('gestion/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('gestion/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    #path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
]