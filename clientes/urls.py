# clientes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registrar_cliente, name='registrar_cliente'),
    path('listar/', views.listar_clientes, name='listar_clientes'),
    path('editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('baja/<int:cliente_id>/', views.dar_baja_cliente, name='dar_baja_cliente'),
    path('reactivar/<int:cliente_id>/', views.reactivar_cliente, name='reactivar_cliente'),
]