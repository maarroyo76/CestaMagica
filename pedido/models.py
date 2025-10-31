import uuid
from django.conf import settings
from django.db import models

from Inventario.models import Producto

# Create your models here.
class Pedido(models.Model):

    ESTADOS = [
        ('PAG', 'Pagado'),
        ('PRE', 'En preparación'),
        ('RET', 'Pendiente de retiro'),
        ('ENT', 'Entregado'),
        ('CAN', 'Cancelado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=4, choices=ESTADOS, default='PEND')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_retiro = models.CharField(max_length=50, blank=True)
    notas = models.TextField(blank=True, null=True)
    metodo_pago = models.CharField(max_length=50, blank=True)
    codigo_pedido = models.CharField(max_length=20, unique=True, blank=True)
    token_ws = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.codigo_pedido:
            self.codigo_pedido = self.generar_codigo_pedido()
        super().save(*args, **kwargs)

    def generar_codigo_pedido(self):
        import random, string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def __str__(self):
        return f"Pedido {self.codigo_pedido} - {self.usuario}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} ({self.pedido.codigo_pedido})"