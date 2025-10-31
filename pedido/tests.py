import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from pedido.models import Pedido

User = get_user_model()

class IniciarTestPago(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.pedido = Pedido.objects.create(usuario=self.user, total=5000)
        self.client.force_login(self.user)
        self.base_url = reverse('pedido:iniciar_pago', args=[self.pedido.id])

    def test_pago_correcto(self):
        data = {
            'pedido_id': str(self.pedido.id),
            'monto': '5000',
            'metodo_pago': 'tarjeta',
        }
        url = f"{self.base_url}?test=1"
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn('url_pago', json_data)
        self.assertIn('token', json_data)

    def test_pago_incorrecto(self):
        data = {
            'pedido_id': str(self.pedido.id),
            'monto': 'invalid',
            'metodo_pago': 'tarjeta',
        }
        url = f"{self.base_url}?test=1"
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
