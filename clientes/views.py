# C:\Users\kachu\Python user\Django\tp_ing_soft_ii\clientes\views.py
from django.shortcuts import render, redirect
from .forms import ClientesForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Clientes
from django.shortcuts import get_object_or_404
from .forms import ClientesForm
from django.contrib import messages
from django.db.models import Q

@login_required
def registrar_cliente(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("No tenés permisos para acceder a esta vista.")
    if request.method == 'POST':
        form = ClientesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_cliente')
    else:
        form = ClientesForm()

    return render(request, 'clientes/registro.html', {'form': form})

@login_required
def listar_clientes(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("No tenés permisos para acceder a esta vista.")

    query = request.GET.get('q')
    if query:
        clientes = Clientes.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        clientes = Clientes.objects.all()

    return render(request, 'clientes/listado.html', {'clientes': clientes, 'query': query})

@login_required
def editar_cliente(request, cliente_id):
    if not request.user.is_superuser:
        return render(request, 'no_autorizado.html')

    cliente = get_object_or_404(Clientes, id=cliente_id)

    if request.method == 'POST':
        form = ClientesForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClientesForm(instance=cliente)

    return render(request, 'clientes/editar.html', {'form': form, 'cliente': cliente})

@login_required
def dar_baja_cliente(request, cliente_id):
    if not request.user.is_staff:
        return redirect('/')

    cliente = get_object_or_404(Clientes, id=cliente_id)
    cliente.estado = False
    cliente.save()
    messages.success(request, f'Cliente {cliente.nombre} {cliente.apellido} dado de baja correctamente.')
    return redirect('listar_clientes')

@login_required
def reactivar_cliente(request, cliente_id):
    if not request.user.is_staff:
        return redirect('/')

    cliente = get_object_or_404(Clientes, id=cliente_id)
    cliente.estado = True
    cliente.save()
    messages.success(request, f'Cliente {cliente.nombre} {cliente.apellido} reactivado correctamente.')
    return redirect('listar_clientes')
