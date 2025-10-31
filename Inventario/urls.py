from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.productos, name='productos'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('search-autocomplete/', views.search_autocomplete, name='search_autocomplete'),
    
    path('contacto/', views.contacto, name='contacto'),
    path('registro/', views.registro, name='registro'),

    path('iniciar_sesion/', views.inicio_sesion, name='iniciar_sesion'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('perfil/', views.perfil, name='perfil'),

    path('gestion/', views.gestion, name='gestion'),
    path('gestion/agregar/', views.agregar_producto, name='agregar_producto'),
    path('gestion/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('gestion/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('gestion/carga_masiva/', views.carga_masiva, name='carga_masiva'),
    path('gestion/descargar_plantilla/', views.descargar_plantilla_productos, name='descargar_plantilla'),

    path('carrito/', include(('Cart.urls', 'cart'), namespace='cart')),
    path('pedido/', include(('pedido.urls', 'pedido'), namespace='pedido')),

    path('marcas/agregar/', views.agregar_marca, name='agregar_marca'),
    path('marcas/editar/<int:marca_id>/', views.editar_marca, name='editar_marca'),
    path('marcas/eliminar/<int:marca_id>/', views.eliminar_marca, name='eliminar_marca'),

    path('categorias/agregar/', views.agregar_categoria, name='agregar_categoria'),
    path('categorias/editar/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),

    path('pedidos/actualizar_estado/<uuid:pedido_id>/', views.actualizar_estado_pedido, name='actualizar_estado_pedido'),
    path('historial/', views.historial_pedidos, name='historial_pedidos'),
    path('recomprar/<uuid:pedido_id>/', views.recomprar_pedido, name='recomprar_pedido'),
]