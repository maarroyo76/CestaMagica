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
    path('marcas/agregar/', views.agregar_marca, name='agregar_marca'),
    path('marcas/editar/<int:marca_id>/', views.editar_marca, name='editar_marca'),
    path('marcas/eliminar/<int:marca_id>/', views.eliminar_marca, name='eliminar_marca'),
    path('categorias/agregar/', views.agregar_categoria, name='agregar_categoria'),
    path('categorias/editar/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('pedidos/actualizar_estado/<uuid:pedido_id>/', views.actualizar_estado_pedido, name='actualizar_estado_pedido'),
]