"""
URL configuration for confir project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# config/urls.py o cafe_el_mejor/urls.py
from django.contrib import admin
from django.urls import path, include
from usuarios.views import login_usuario, inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clientes/', include('clientes.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('login/', login_usuario, name='login'),
    path('clientes/', include('clientes.urls')), 
    path('', inicio, name='inicio'),
    path('inicio/', inicio, name='inicio'),
    path('productos/', include('productos.urls')),  
    path('proveedores/', include('proveedores.urls')),
    path('ordenes/', include('ordenes_compra.urls')),
    path('facturacion/', include('facturacion.urls')),
    path('cobranzas/', include('cobranzas.urls')),   
]
