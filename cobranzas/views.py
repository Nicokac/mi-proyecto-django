# cobranzas\views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CobranzaForm
from facturacion.models import Factura
from clientes.models import Clientes
from cobranzas.models import Cobranza
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib import messages

@login_required
def registrar_cobranza(request):
    try:
        cliente = Clientes.objects.get(usuario=request.user)
    except Clientes.DoesNotExist:
        return redirect('inicio')  # o mostrar un mensaje de error

    if request.method == 'POST':
        form = CobranzaForm(request.POST, cliente=cliente)
        if form.is_valid():
            cobranza = form.save(commit=False)

            # 🔐 Validación adicional (refuerzo de seguridad)
            if cobranza.factura.cliente != cliente:
                form.add_error('factura', 'No puedes registrar una cobranza para otra persona.')
            else:
                cobranza.cliente = cliente
                cobranza.fecha_pago = datetime.now()
                cobranza.save()
                messages.success(request, "✅ Cobranza registrada exitosamente.")
                return redirect('listar_cobranzas')
    else:
        form = CobranzaForm(cliente=cliente)

    # 🔒 Solo las facturas del cliente logueado
    facturas = Factura.objects.filter(cliente=cliente)
    facturas_json = json.dumps({str(f.id): float(f.total) for f in facturas}, cls=DjangoJSONEncoder)

    return render(request, 'cobranzas/registro.html', {
        'form': form,
        'facturas_json': facturas_json
    })


@login_required
def listar_cobranzas(request):
    cobranzas = Cobranza.objects.all().select_related('factura', 'cliente')

    # Filtros
    numero = request.GET.get('numero')
    cliente_id = request.GET.get('cliente')
    tipo_pago = request.GET.get('tipo_pago')

    if numero:
        cobranzas = cobranzas.filter(factura__numero__icontains=numero)

    if request.user.is_staff and cliente_id:
        cobranzas = cobranzas.filter(cliente__id=cliente_id)
    elif not request.user.is_staff:
        try:
            cliente = Clientes.objects.get(usuario=request.user)
            cobranzas = cobranzas.filter(cliente=cliente)
        except Clientes.DoesNotExist:
            cobranzas = Cobranza.objects.none()

    if tipo_pago:
        cobranzas = cobranzas.filter(tipo_pago=tipo_pago)

    # Datos para los filtros
    clientes = Clientes.objects.all() if request.user.is_staff else None
    TIPOS_PAGO = Cobranza.obtener_tipos_pago()  # Acceso correcto a los tipos de pago

    return render(request, 'cobranzas/listado.html', {
        'cobranzas': cobranzas,
        'clientes': clientes,
        'TIPOS_PAGO': TIPOS_PAGO,
        'filtros': {
            'numero': numero,
            'cliente': cliente_id,
            'tipo_pago': tipo_pago
        }
    })

@login_required
def modificar_cobranza(request, cobranza_id):
    try:
        cobranza = Cobranza.objects.select_related('factura', 'cliente').get(id=cobranza_id)
        if not request.user.is_staff:
            cliente = Clientes.objects.get(usuario=request.user)
            if cobranza.cliente != cliente:
                messages.error(request, "No tiene permiso para modificar esta cobranza.")
                return redirect('listar_cobranzas')
        else:
            cliente = cobranza.cliente

        if cobranza.factura.estado != 'pendiente':
            messages.error(request, "Solo se pueden modificar cobranzas asociadas a facturas pendientes.")
            return redirect('listar_cobranzas')

    except Cobranza.DoesNotExist:
        messages.error(request, "La cobranza no existe.")
        return redirect('listar_cobranzas')

    if request.method == 'POST':
        form = CobranzaForm(request.POST, instance=cobranza, cliente=cliente)
        if form.is_valid():
            cobranza.tipo_pago = form.cleaned_data['tipo_pago']
            cobranza.save()
            messages.success(request, "Cobranza modificada correctamente.")
            return redirect('listar_cobranzas')
    else:
        form = CobranzaForm(instance=cobranza, cliente=cliente)
        # QUITAR ESTAS DOS LÍNEAS ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        # form.fields['factura'].disabled = True
        # form.fields['monto'].disabled = True
    factura_obj = cobranza.factura

    return render(request, 'cobranzas/modificar.html', {
        'form': form,
        'cobranza': cobranza,
        'factura_obj': factura_obj,
    })



