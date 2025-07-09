# Create your views here.
# productos/views.py
from django.shortcuts import render, redirect
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Producto
from django.shortcuts import get_object_or_404
from django.db.models import Q
from proveedores.models import Proveedor

@login_required
def registrar_producto(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("No tenés permisos para acceder a esta vista.")            

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            nuevo_producto = form.save(commit=False)
            proveedor_default = Proveedor.objects.get(nombre__iexact="Cafe El Mejor")
            nuevo_producto.proveedor = proveedor_default
            nuevo_producto.save()
            return redirect('/inicio')
    else:
        form = ProductoForm()
    return render(request, 'productos/registro.html', {'form': form})

@login_required
def listar_productos(request):
    query = request.GET.get('q')
    if request.user.is_staff:
        qs = Producto.objects.all()
    else:
        qs = Producto.objects.filter(proveedor__nombre__iexact="Cafe El Mejor")
    if query:
        productos = qs.filter(
            Q(nombre__icontains=query) |
            Q(sku__icontains=query) |
            Q(precio__icontains=query)
        )
    else:
        productos = qs
    return render(request, 'productos/listado.html', {'productos': productos, 'query': query})

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ProductoForm(request.POST, instance=producto)
            if form.is_valid():
                form.save()
                return redirect('listar_productos')
        else:
            form = ProductoForm(instance=producto)
        return render(request, 'productos/formulario.html', {'form': form, 'editar': True})
    return redirect('listar_productos')

@login_required
def dar_baja_producto(request, producto_id):
    if request.user.is_superuser:
        producto = get_object_or_404(Producto, id=producto_id)
        producto.delete()
    return redirect('listar_productos')

@login_required
def reactivar_producto(request, producto_id):
    if request.user.is_superuser:
        producto = get_object_or_404(Producto, id=producto_id)
        producto.estado = True
        producto.save()
    return redirect('listar_productos')
