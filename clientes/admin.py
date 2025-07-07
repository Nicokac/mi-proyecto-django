from django.contrib import admin
from django.contrib import admin
from .models import Clientes

# Register your models here.

@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'estado', 'usuario')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('estado',)
    list_editable = ('estado',)