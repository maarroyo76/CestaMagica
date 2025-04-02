from django.contrib import admin
from .models import Producto, Categoria, Marca, userProfile, UnidadVenta, PrecioProducto

class PrecioProductoInline(admin.TabularInline):
    model = PrecioProducto
    extra = 1

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'stock', 'mostrar_precios', 'categoria', 'marca')
    list_filter = ('categoria', 'marca')
    search_fields = ('nombre', 'descripcion')
    inlines = [PrecioProductoInline] 

    def mostrar_precios(self, obj):
        return ", ".join([f"{pp.unidad_venta.nombre}: ${pp.precio}" for pp in obj.precios.all()])
    mostrar_precios.short_description = 'Precios' 

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(userProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefono', 'role')
    search_fields = ('user__username', 'telefono', 'role')

@admin.register(UnidadVenta)
class UnidadVentaAdmin(admin.ModelAdmin):
    list_display = ('nombre',) 
    search_fields = ('nombre',)

@admin.register(PrecioProducto)
class PrecioProductoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'unidad_venta', 'precio')
    search_fields = ('producto__nombre', 'unidad_venta__nombre')