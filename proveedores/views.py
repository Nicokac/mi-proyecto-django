# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProveedorForm
from django.http import HttpResponseForbidden
from .models import Proveedor
from django.shortcuts import get_object_or_404
from django.db.models import Q

@login_required
def registrar_proveedor(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("No tenés permisos para acceder a esta vista.")
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/registro.html', {'form': form})

def es_admin(user):
    return user.is_superuser

@login_required
def listar_proveedores(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tenés permisos para acceder a esta vista.")
    query = request.GET.get('q')
    if query:
        proveedores = Proveedor.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(telefono__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        proveedores = Proveedor.objects.all()

        proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/listado.html', {'proveedores': proveedores})

@login_required
@user_passes_test(es_admin)
def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/formulario.html', {'form': form, 'editar': True})

@login_required
def dar_baja_proveedor(request, proveedor_id):
    if request.user.is_superuser:
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)
        proveedor.estado = False
        proveedor.save()
    return redirect('listar_proveedores')

@login_required
def reactivar_proveedor(request, proveedor_id):
    if request.user.is_superuser:
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)
        proveedor.estado = True
        proveedor.save()
    return redirect('listar_proveedores')
