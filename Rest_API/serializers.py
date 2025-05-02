import rest_framework
from rest_framework import serializers
from Inventario.models import Producto, Categoria, Marca

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'stock', 'precio','imagen', 'categoria', 'marca', 'destacado']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['nombre']

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['nombre']
