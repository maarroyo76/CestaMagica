from django.shortcuts import render
from Inventario.models import Producto, Categoria, Marca, UnidadVenta, PrecioProducto
from .serializers import ProductoSerializer, CategoriaSerializer, MarcaSerializer, UnidadVentaSerializer, PrecioProductoSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
@api_view(['GET', 'POST'])
def lista_productos(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)

        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer=data, status=status.HTTP_201_CREATED)
        else:
            print("Error", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def vista_producto(request, id):
    try:
        producto = Producto.objects.get(id=id)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print("Error", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'POST'])
def lista_categorias(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)

        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CategoriaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer=data, status=status.HTTP_201_CREATED)
        else:
            print("Error", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def vista_categoria(request, id):
    try:
        categoria = Categoria.objects.get(id=id)
    except Categoria.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print("Error", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@csrf_exempt
@api_view(['GET', 'POST'])
def lista_marcas(request):
    if request.method == 'GET':
        marcas = Producto.objects.all()
        serializer = MarcaSerializer(marcas, many=True)

        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MarcaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer=data, status=status.HTTP_201_CREATED)
        else:
            print("Error", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def vista_marca(request, id):
    try:
        marca = Marca.objects.get(id=id)
    except Marca.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MarcaSerializer(marca)
        return Response(serializer.data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = MarcaSerializer(marca, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print("Error", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        marca.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@csrf_exempt
@api_view(['GET', 'POST'])
def lista_unidades_venta(request):
    if request.method == 'GET':
        unidades_venta = UnidadVenta.objects.all()
        serializer = UnidadVentaSerializer(unidades_venta, many=True)

        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UnidadVentaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer=data, status=status.HTTP_201_CREATED)
        else:
            print("Error", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def vista_unidad_venta(request, id):
    try:
        unidad_venta = UnidadVenta.objects.get(id=id)
    except UnidadVenta.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UnidadVentaSerializer(unidad_venta)
        return Response(serializer.data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = UnidadVentaSerializer(unidad_venta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print("Error", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        unidad_venta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'POST'])
def lista_precio_productos(request):
    if request.method == 'GET':
        precio_productos = PrecioProducto.objects.all()
        serializer = PrecioProductoSerializer(precio_productos, many=True)

        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PrecioProductoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer=data, status=status.HTTP_201_CREATED)
        else:
            print("Error", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def vista_precio_producto(request, id):
    try:
        precio_producto = PrecioProducto.objects.get(id=id)
    except PrecioProducto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PrecioProductoSerializer(precio_producto)
        return Response(serializer.data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = PrecioProductoSerializer(precio_producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print("Error", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        precio_producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

