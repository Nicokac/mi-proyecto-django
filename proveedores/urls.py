from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registrar_proveedor, name='registrar_proveedor'),
    path('listar/', views.listar_proveedores, name='listar_proveedores'),
    path('editar/<int:proveedor_id>/', views.editar_proveedor, name='editar_proveedor'),
    path('baja/<int:proveedor_id>/', views.dar_baja_proveedor, name='dar_baja_proveedor'),
    path('reactivar/<int:proveedor_id>/', views.reactivar_proveedor, name='reactivar_proveedor'),
]