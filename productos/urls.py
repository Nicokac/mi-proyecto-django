#productos\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registrar_producto, name='registrar_producto'),
    path('listado/', views.listar_productos, name='listar_productos'),
    path('editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('baja/<int:producto_id>/', views.dar_baja_producto, name='dar_baja_producto'),
    path('reactivar/<int:producto_id>/', views.reactivar_producto, name='reactivar_producto'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('actualizar_carrito/', views.actualizar_carrito, name='actualizar_carrito'),
]