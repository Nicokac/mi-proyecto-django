# facturacion\models.py
from django.db import models
from clientes.models import Clientes
from productos.models import Producto
from ordenes_compra.models import OrdenDeCompra

# Create your models here.
class Factura(models.Model):
    ESTADOS_FACTURA = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
    ]
    numero = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    orden = models.OneToOneField('ordenes_compra.OrdenDeCompra', on_delete=models.CASCADE, null=True, blank=True)  # ✅ AÑADIDO
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADOS_FACTURA, default='pendiente')

    def __str__(self):
        return f"Factura {self.numero} - {self.cliente.nombre}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)