from django.contrib import admin
from django.contrib import admin
from .models import Factura, DetalleFactura

# Register your models here.

class DetalleFacturaInline(admin.TabularInline):
    model = DetalleFactura
    extra = 1

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    inlines = [DetalleFacturaInline]
