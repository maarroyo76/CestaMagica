from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    id_tienda = models.IntegerField(default=0)
    descripcion = models.TextField(default="")
    stock = models.IntegerField(default=0)
    precio = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', default='productos/default.png')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    destacado = models.BooleanField(default=False)

    STOCK_UMBRAL_MINIMO = 3

    @property
    def is_available(self):
        return self.stock > self.STOCK_UMBRAL_MINIMO
    
    @property
    def stock_vendible(self):
        if self.is_available:
            return self.stock - self.STOCK_UMBRAL_MINIMO
        return 0
    
    def __str__(self):
        return self.nombre

class userProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=settings.ROLES)

    def __str__(self):
        return self.user.username
