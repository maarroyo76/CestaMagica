import json
from django.test import TestCase
from django.urls import reverse
from Inventario.models import Producto, Marca, Categoria

class ProductoAPITests(TestCase):
    def setUp(self):
        self.marca = Marca.objects.create(nombre='MarcaTest')
        self.categoria = Categoria.objects.create(nombre='CategoriaTest')
        self.list_url = reverse('lista_productos')
        
        self.producto = Producto.objects.create(
            nombre='ProductoTest',
            marca=self.marca,
            precio=10000,
            categoria=self.categoria,
        )
        self.detail_url = reverse('vista_producto', args=[self.producto.id])

    def test_get_productos_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('ProductoTest', response.content.decode())

    def test_get_producto_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('ProductoTest', response.content.decode())

    def test_create_producto(self):
        data = {
            'nombre': 'NuevoProducto',
            'marca': self.marca.id,
            'precio': 5000,
            'categoria': self.categoria.id,
        }
        response = self.client.post(
            self.list_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Producto.objects.filter(nombre='NuevoProducto').exists())

    def test_update_producto(self):
        data = {
            'nombre': 'ProductoActualizado',
            'marca': self.marca.id,
            'precio': 15000,
            'categoria': self.categoria.id,
        }
        response = self.client.put(
            self.detail_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'ProductoActualizado')
