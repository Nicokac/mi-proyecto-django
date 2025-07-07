# usuarios/urls.py
from django.urls import path
from . import views
from .views import inicio

urlpatterns = [
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('login/', views.login_usuario, name='login_usuario'),  # Agregada
    path('logout/', views.logout_usuario, name='logout'),
    path('', inicio, name='inicio'),   
]
