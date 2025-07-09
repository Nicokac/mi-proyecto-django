#C:\Users\kachu\Python user\Django\tp_ing_soft_ii\ordenes_compra\views.py
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django import forms
from django.http import HttpResponseForbidden
import json
from .forms import OrdenDeCompraForm, DetalleOrdenFormSet, DetalleOrdenForm
from .models import OrdenDeCompra
from productos.models import Producto
from proveedores.models import Proveedor
from .models import ModificacionOrden, DetalleOrden
# Vista: registrar_orden_compra (dentro del bloque if request.method == 'POST')
from facturacion.models import Factura
from clientes.models import Clientes
from django.forms import inlineformset_factory
from functools import partial

@login_required
def registrar_orden_compra(request):
    producto_id = request.GET.get('producto_id')
    initial_data = []

    if request.method == 'POST':
        # --- Recuperar el carrito si sos cliente, para el formset dinámico ---
        if not request.user.is_staff:
            carrito = request.session.get('carrito', {})
            if carrito:
                initial_data = [
                    {'producto': int(pid), 'cantidad': cantidad}
                    for pid, cantidad in carrito.items()
                ]
            elif producto_id:
                initial_data = [{'producto': producto_id}]
        # Para admin, que sea 1 por default
        DetalleOrdenFormSetCarrito = inlineformset_factory(
            OrdenDeCompra,
            DetalleOrden,
            form=DetalleOrdenForm,
            extra=max(1, len(initial_data)),  # mínimo 1 por si viene vacío
            can_delete=True
        )
        form = OrdenDeCompraForm(request.POST)

        # 1. Guardar orden con commit=False (todavía no en DB)
        if form.is_valid():
            orden = form.save(commit=False)
            if not request.user.is_staff:
                cliente_obj = Clientes.objects.get(usuario=request.user)
                orden.cliente = cliente_obj
                proveedor_default = Proveedor.objects.get(nombre__iexact="Cafe El Mejor")
                orden.proveedor = proveedor_default
                orden.tipo = 'cliente'
            else:
                orden.tipo = 'proveedor'

            orden.save()  # 2. ¡Ahora la orden ya tiene ID!

            # 3. Ahora sí: inicializamos el formset, pero le pasamos instance=orden
            formset = DetalleOrdenFormSetCarrito(request.POST, instance=orden)

            # --- Filtrar productos solo “Cafe El Mejor” si es cliente ---
            if not request.user.is_staff:
                proveedor_cafe = Proveedor.objects.get(nombre__iexact="Cafe El Mejor")
                for f in formset.forms:
                    f.fields['producto'].queryset = Producto.objects.filter(estado=True, proveedor=proveedor_cafe)
            # ----------------------------------------------------------

            print("POST recibido:", request.POST)
            if formset.is_valid():
                print("✅ Formularios válidos")
                with transaction.atomic():
                    detalles = formset.save(commit=False)
                    for detalle in detalles:
                        detalle.precio_unitario = detalle.producto.precio
                        detalle.save()
                        if orden.tipo == 'proveedor':
                            detalle.producto.stock += detalle.cantidad
                        else:
                            detalle.producto.stock -= detalle.cantidad
                        detalle.producto.save()

                    # 🧾 Crear factura automáticamente si es cliente (ahora con precios asignados)
                    if orden.tipo == 'cliente':
                        ultimo_numero = Factura.objects.count() + 1
                        numero_factura = f"F-{ultimo_numero:06d}"

                        total_factura = sum(
                            detalle.precio_unitario * detalle.cantidad
                            for detalle in detalles
                        )

                        factura = Factura.objects.create(
                            numero=numero_factura,
                            cliente=orden.cliente,
                            total=total_factura,
                            orden=orden
                        )
                    # --- LIMPIAR EL CARRITO LUEGO DE CONFIRMAR ORDEN ---
                    if not request.user.is_staff:
                        request.session['carrito'] = {}

                    messages.success(request, 'Orden de compra registrada correctamente.')
                    return redirect('listar_ordenes')
            else:
                print("❌ Formset inválido")
                for f in formset:
                    print(f.errors)
        else:
            print("❌ Formulario OrdenDeCompra inválido")
            print("Errores:", form.errors)
    else:
        print("📄 GET recibido")
        if request.user.is_staff:
            proveedores = Proveedor.objects.exclude(nombre__iexact="Cafe El Mejor")
            form = OrdenDeCompraForm()
            form.fields['proveedor'].queryset = proveedores
            formset = inlineformset_factory(
                OrdenDeCompra,
                DetalleOrden,
                form=DetalleOrdenForm,
                extra=1,
                can_delete=True
            )()
        else:
            form = OrdenDeCompraForm()
            form.fields['proveedor'].widget = forms.HiddenInput()
            carrito = request.session.get('carrito', {})
            if carrito:
                initial_data = [
                    {'producto': int(pid), 'cantidad': cantidad}
                    for pid, cantidad in carrito.items()
                ]
            elif producto_id:
                initial_data = [{'producto': producto_id}]
            # --- El formset con la cantidad de productos del carrito ---
            DetalleOrdenFormSetCarrito = inlineformset_factory(
                OrdenDeCompra,
                DetalleOrden,
                form=DetalleOrdenForm,
                extra=max(1, len(initial_data)),
                can_delete=True
            )
            formset = DetalleOrdenFormSetCarrito(initial=initial_data)
            # --- Filtrar productos solo “Cafe El Mejor” si es cliente ---
            proveedor_cafe = Proveedor.objects.get(nombre__iexact="Cafe El Mejor")
            for f in formset.forms:
                f.fields['producto'].queryset = Producto.objects.filter(estado=True, proveedor=proveedor_cafe)
            # ----------------------------------------------------------

    if not request.user.is_staff:
        proveedor_default = Proveedor.objects.get(nombre__iexact="Cafe El Mejor")
        productos_activos = Producto.objects.filter(estado=True, proveedor=proveedor_default)
    else:
        productos_activos = Producto.objects.filter(estado=True)

    productos_dict = {str(p.id): float(p.precio) for p in productos_activos}
    productos_stock = {str(p.id): p.stock for p in productos_activos}

    return render(request, 'ordenes_compra/registro.html', {
        'form': form,
        'formset': formset,
        'productos': list(productos_activos),
        'productos_json': json.dumps(productos_dict),
        'stocks_json': json.dumps(productos_stock),
        'productos_dict': productos_dict,
    })

@login_required
def listar_ordenes(request):
    ordenes = OrdenDeCompra.objects.all().order_by('-fecha_emision')

    query = request.GET.get("q")
    proveedor_id = request.GET.get("proveedor")
    fecha_desde = request.GET.get("desde")
    fecha_hasta = request.GET.get("hasta")

    if query:
        ordenes = ordenes.filter(id=query.strip())

    if request.user.is_staff and proveedor_id:
        ordenes = ordenes.filter(proveedor__id=proveedor_id)

    if fecha_desde:
        ordenes = ordenes.filter(fecha_emision__date__gte=fecha_desde)

    if fecha_hasta:
        ordenes = ordenes.filter(fecha_emision__date__lte=fecha_hasta)

    proveedores = Proveedor.objects.all() if request.user.is_staff else None

    return render(request, 'ordenes_compra/listado.html', {
        'ordenes': ordenes,
        'query': query,
        'proveedor_id': proveedor_id,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'proveedores': proveedores
    })

@login_required
def detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenDeCompra, pk=orden_id)
    return render(request, 'ordenes_compra/detalle.html', {'orden': orden})

@login_required
def dar_baja_orden(request, orden_id):
    orden = get_object_or_404(OrdenDeCompra, id=orden_id)
    if orden.estado:
        orden.estado = False
        orden.motivo_baja = 'Baja solicitada por el usuario'
        orden.save()
        messages.success(request, f'Orden #{orden.id} dada de baja correctamente.')
    return redirect('listar_ordenes')

@login_required
def modificar_orden(request, orden_id):
    orden = get_object_or_404(OrdenDeCompra, pk=orden_id)

    if not request.user.is_staff:
        return HttpResponseForbidden("No tenés permiso para modificar esta orden.")

    if request.method == 'POST':
        form = OrdenDeCompraForm(request.POST, instance=orden)
        formset = DetalleOrdenFormSet(request.POST, instance=orden)
        print("📝 POST recibido para modificación de orden")
        print("POST recibido:", request.POST)
        print("Formset errores:", formset.errors if 'formset' in locals() else 'no hay formset')
        if form.is_valid() and formset.is_valid():
            # Validación extra: al menos un detalle con producto y cantidad válida
            detalles_data = formset.cleaned_data
            detalles_validos = [d for d in detalles_data if d and d.get('producto') and d.get('cantidad')]

            if not detalles_validos:
                messages.error(request, 'Debés ingresar al menos un producto con cantidad válida.')
            else:
                with transaction.atomic():
                    # Forzar campos clave antes de guardar
                    if not request.user.is_staff:
                        form.instance.proveedor = orden.proveedor
                        form.instance.tipo = 'cliente'
                    else:
                        form.instance.tipo = 'proveedor'

                    form.save()

                    # Revertir stock previo
                    for detalle in orden.detalles.all():
                        if orden.tipo == 'proveedor':
                            detalle.producto.stock -= detalle.cantidad
                        else:
                            detalle.producto.stock += detalle.cantidad
                        detalle.producto.save()

                    orden.detalles.all().delete()

                    # Guardar nuevos detalles
                    detalles = formset.save(commit=False)
                    for detalle in detalles:
                        detalle.orden = orden
                        detalle.precio_unitario = detalle.producto.precio
                        detalle.save()

                        if orden.tipo == 'proveedor':
                            detalle.producto.stock += detalle.cantidad
                        else:
                            detalle.producto.stock -= detalle.cantidad

                        detalle.producto.save()

                    # Registrar historial de cambios
                    productos_modificados = ", ".join([f"{d.producto.nombre} (x{d.cantidad})" for d in detalles])
                    ModificacionOrden.objects.create(
                        orden=orden,
                        usuario=request.user,
                        descripcion=f"Orden modificada. Productos: {productos_modificados}"
                    )

                    messages.success(request, f'Orden #{orden.id} modificada con éxito.')
                    return redirect('listar_ordenes')
        else:
            print("❌ Formulario inválido")
            print("Errores OrdenDeCompraForm:", form.errors.as_data())
            print("Errores DetalleOrdenFormSet:", formset.errors)
            print("Campos enviados:", request.POST)
            messages.error(request, 'Hay errores en el formulario.')
    else:
        form = OrdenDeCompraForm(instance=orden)
        formset = DetalleOrdenFormSet(instance=orden)

    productos_dict = {str(p.id): float(p.precio) for p in Producto.objects.filter(estado=True)}
    return render(request, 'ordenes_compra/modificar.html', {
        'form': form,
        'formset': formset,
        'orden': orden,
        'productos_json': json.dumps(productos_dict),
    })



