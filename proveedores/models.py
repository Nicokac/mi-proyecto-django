from django.db import models
# Create your models here.

class Proveedor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
