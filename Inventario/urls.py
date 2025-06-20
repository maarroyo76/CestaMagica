from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.productos, name='productos'),
    path('gestion/', views.gestion, name='gestion'),
    path('contacto/', views.contacto, name='contacto'),
    path('registro/', views.registro, name='registro'),
    path('iniciar_sesion/', views.inicio_sesion, name='iniciar_sesion'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('gestion/agregar/', views.agregar_producto, name='agregar_producto'),
    path('gestion/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('gestion/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('perfil/', views.perfil, name='perfil'),
    path('carrito/', include(('Cart.urls', 'cart'), namespace='cart')),
    path('pedido/', include(('pedido.urls', 'pedido'), namespace='pedido')),
]

handler404 = views.error_404_view
handler500 = views.error_500_view
handler403 = views.error_403_view
handler400 = views.error_400_view