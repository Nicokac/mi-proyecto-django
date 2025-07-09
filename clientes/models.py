# clientes\models.py
from django.db import models
from django.conf import settings

# Create your models here.
class Clientes(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    contrasenia = models.CharField(max_length=128)
    estado = models.BooleanField(default=True) # Activo/Inactivo
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido} {self.email}'