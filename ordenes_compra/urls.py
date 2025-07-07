#ordenes_compra\urls.py
from django.urls import path
from .views import registrar_orden_compra, listar_ordenes, detalle_orden, dar_baja_orden, modificar_orden

urlpatterns = [
    path('registro/', registrar_orden_compra, name='registrar_orden'),
    path('listar/', listar_ordenes, name='listar_ordenes'),
    path('detalle/<int:orden_id>/', detalle_orden, name='detalle_orden'),
    path('baja/<int:orden_id>/', dar_baja_orden, name='dar_baja_orden'),
    path('modificar/<int:orden_id>/', modificar_orden, name='modificar_orden'),
]
