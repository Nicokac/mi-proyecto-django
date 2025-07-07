#cobranzas\models.py
from django.db import models
from django.db import models
from facturacion.models import Factura
from clientes.models import Clientes

# Create your models here.

class Cobranza(models.Model):
    METODO_PAGO_CHOICES = [
        ('debito', 'Débito'),
        ('credito', 'Crédito'),
        ('qr', 'QR'),
    ]

    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    tipo_pago = models.CharField(max_length=10, choices=METODO_PAGO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cobranza #{self.id} - Factura {self.factura.numero}"

    @classmethod
    def obtener_tipos_pago(cls):
        return cls.METODO_PAGO_CHOICES