from django.contrib import admin
from .models import Producto, Categoria, Marca, User

# Register your models here.

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'stock', 'precio', 'categoria', 'marca')
    list_filter = ('categoria', 'marca')
    search_fields = ('nombre', 'descripcion')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
