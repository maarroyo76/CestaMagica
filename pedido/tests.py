from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from pedido.models import Pedido

User = get_user_model()

class IniciarTestPago(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.pedido = Pedido.objects.create(
            usuario=self.user,
            total=5000,
        )
        self.client.login(username='testuser', password='testpass')

    def test_iniciar_pago(self):
        url = reverse('pedido:iniciar_pago', kwargs={'pedido_id': str(self.pedido.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('token_ws', Pedido.objects.get(id=self.pedido.id).__dict__)

    def test_confirmar_pedido(self):
        self.pedido.estado = 'PAG'
        self.pedido.save()

        url = reverse('pedido:pedido_exito', kwargs={'pedido_id': str(self.pedido.id)})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pedido")