# Create your views here.
# productos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Producto
from django.db.models import Q
from proveedores.models import Proveedor
from django.contrib import messages

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

@login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = Producto.objects.filter(id__in=carrito.keys())
    carrito_items = []
    for producto in productos:
        cantidad = carrito.get(str(producto.id), 0)
        carrito_items.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': producto.precio * cantidad
        })
    total = sum(item['subtotal'] for item in carrito_items)
    return render(request, 'productos/ver_carrito.html', {'carrito_items': carrito_items, 'total': total})

@login_required
def actualizar_carrito(request):
    if request.method == "POST":
        carrito = request.session.get('carrito', {})
        for key in list(carrito.keys()):
            nueva_cant = int(request.POST.get(f'cantidad_{key}', 0))
            if nueva_cant > 0:
                producto = get_object_or_404(Producto, pk=key)
                carrito[key] = min(nueva_cant, producto.stock)
            else:
                carrito.pop(key)
        request.session['carrito'] = carrito
        messages.success(request, "Carrito actualizado.")
    return redirect('ver_carrito')

@login_required
def agregar_al_carrito(request, producto_id):
    if request.method == "POST":
        cantidad = int(request.POST.get('cantidad', 1))
        carrito = request.session.get('carrito', {})

        producto = get_object_or_404(Producto, pk=producto_id)
        cantidad = min(cantidad, producto.stock)

        if str(producto_id) in carrito:
            nueva_cant = carrito[str(producto_id)] + cantidad
            carrito[str(producto_id)] = min(nueva_cant, producto.stock)
        else:
            carrito[str(producto_id)] = cantidad

        request.session['carrito'] = carrito
        messages.success(request, f"{producto.nombre} agregado al carrito.")
    return redirect('listar_productos')
