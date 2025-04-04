import rest_framework
from rest_framework import serializers
from Inventario.models import Producto, Categoria, Marca, PrecioProducto, UnidadVenta

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'stock', 'imagen', 'categoria', 'marca', 'destacado']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['nombre']

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['nombre']

class PrecioProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecioProducto
        fields = ['producto', 'unidad_venta', 'precio']

class UnidadVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadVenta
        fields = ['nombre']
