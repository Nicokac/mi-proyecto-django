# Create your views here.
# usuarios/views.py
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm
from .models import Usuario

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])

            # Aseguramos que sea cliente (no admin)
            usuario.is_staff = False
            usuario.is_superuser = False
            usuario.estado = True
            usuario.is_active = True

            usuario.save()
            return redirect('/inicio')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip().lower()
            password = form.cleaned_data['password']
            usuario = authenticate(request, email=email, password=password)

            print(f'Autenticando: {email} / {password}')
            print('Resultado:', usuario)

            if usuario is not None:
                # Si es staff o superuser, lo dejamos pasar siempre
                if usuario.is_staff or usuario.is_superuser:
                    login(request, usuario)
                    return redirect('/')
                # Chequear si es cliente y si está activo
                try:
                    from clientes.models import Clientes
                    cliente = Clientes.objects.get(usuario=usuario)
                    if not cliente.estado:
                        form.add_error(None, 'Tu cuenta está inactiva. Consultá con el administrador.')
                        return render(request, 'usuarios/login.html', {'form': form})
                except Clientes.DoesNotExist:
                    # No es cliente asociado
                    pass

                login(request, usuario)
                return redirect('/')
            else:
                form.add_error(None, 'Email o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('/login')

@login_required
def inicio(request):
    return render(request, 'inicio.html')