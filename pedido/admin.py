from django.contrib import admin

# Register your models here.
from .models import Pedido, DetallePedido
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('codigo_pedido', 'usuario', 'estado', 'total', 'fecha')
    list_filter = ('estado', 'fecha')
    search_fields = ('codigo_pedido', 'usuario__username')
    readonly_fields = ('codigo_pedido', 'token_ws')
    ordering = ('-fecha',)
@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    list_filter = ('pedido__estado', 'producto__categoria')
    search_fields = ('pedido__codigo_pedido', 'producto__nombre')
    readonly_fields = ('subtotal',)
    