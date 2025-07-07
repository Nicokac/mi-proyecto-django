#facturacion\views.py
from django.contrib.auth.decorators import login_required
from .models import Factura
from clientes.models import Clientes
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# Create your views here.

@login_required
def listar_facturas(request):
    facturas = Factura.objects.all().order_by('-fecha')

    # Filtrado
    numero = request.GET.get("numero")
    cliente_id = request.GET.get("cliente")
    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")

    if numero:
        facturas = facturas.filter(numero__icontains=numero)

    if request.user.is_staff:
        if cliente_id:
            facturas = facturas.filter(cliente__id=cliente_id)
    else:
        try:
            cliente = Clientes.objects.get(usuario=request.user)
            facturas = facturas.filter(cliente=cliente)
        except Clientes.DoesNotExist:
            facturas = Factura.objects.none()

    if desde:
        facturas = facturas.filter(fecha__date__gte=desde)
    if hasta:
        facturas = facturas.filter(fecha__date__lte=hasta)

    clientes = Clientes.objects.all() if request.user.is_staff else None

    return render(request, 'facturacion/listado.html', {
        'facturas': facturas,
        'clientes': clientes,
        'filtros': {
            'numero': numero,
            'cliente': cliente_id,
            'desde': desde,
            'hasta': hasta
        }
    })

@login_required
def detalle_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)

    # Si es un cliente, solo puede ver sus propias facturas
    if not request.user.is_staff and factura.cliente.usuario != request.user:
        return render(request, '403.html', status=403)

    return render(request, 'facturacion/detalle.html', {'factura': factura})

@login_required
def modificar_estado_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)

    if not request.user.is_staff:
        messages.error(request, "Solo los administradores pueden modificar el estado de la factura.")
        return redirect('listar_facturas')

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Factura.ESTADOS_FACTURA).keys():
            factura.estado = nuevo_estado
            factura.save()
            messages.success(request, "Estado de factura actualizado correctamente.")
        else:
            messages.error(request, "Estado no válido.")
        return redirect('listar_facturas')

    return render(request, 'facturacion/modificar_estado.html', {'factura': factura})
