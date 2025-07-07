from django.urls import path
from . import views

urlpatterns = [
    path('listado/', views.listar_facturas, name='listar_facturas'),
    path('detalle/<int:factura_id>/', views.detalle_factura, name='detalle_factura'),
    path('factura/<int:factura_id>/modificar_estado/', views.modificar_estado_factura, name='modificar_estado_factura'),
]