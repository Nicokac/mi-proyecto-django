from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registrar_cobranza, name='registrar_cobranza'),
    path('listado/', views.listar_cobranzas, name='listar_cobranzas'),
    path('cobranzas/modificar/<int:cobranza_id>/', views.modificar_cobranza, name='modificar_cobranza'),
    path('baja/<int:cobranza_id>/', views.baja_cobranza, name='baja_cobranza'),
]
