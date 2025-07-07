# usuarios/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .managers import UsuarioManager

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)  # Activo/inactivo
    is_staff = models.BooleanField(default=False)  # Permite acceso al admin
    is_active = models.BooleanField(default=True)  # Habilita inicio de sesión

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.email})'
