#ordenes_compra\models.py
# Create your models here.
from django.db import models
from productos.models import Producto
from proveedores.models import Proveedor
from django import forms
from django.forms import inlineformset_factory
from django.conf import settings
from clientes.models import Clientes  # importalo arriba

class OrdenDeCompra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)
    motivo_baja = models.TextField(blank=True, null=True)
    tipo = models.CharField(
        max_length=20,
        choices=[('cliente', 'Cliente'), ('proveedor', 'Proveedor')],
        default='proveedor'
    )
    cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Orden #{self.id} - {self.proveedor.nombre}'

class DetalleOrden(models.Model):
    orden = models.ForeignKey(OrdenDeCompra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
class ModificacionOrden(models.Model):
    orden = models.ForeignKey(OrdenDeCompra, on_delete=models.CASCADE, related_name='modificaciones')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()

    def __str__(self):
        return f"Modificación de orden #{self.orden.id} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
