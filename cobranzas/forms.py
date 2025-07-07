# cobranzas/forms.py
from django import forms
from .models import Cobranza
from facturacion.models import Factura

class CobranzaForm(forms.ModelForm):
    class Meta:
        model = Cobranza
        fields = ['factura', 'tipo_pago', 'monto']
        widgets = {
            'factura': forms.Select(attrs={'class': 'form-control'}),
            'tipo_pago': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        cliente = kwargs.pop('cliente', None)  # 🔹 nuevo
        super().__init__(*args, **kwargs)

        # 🔹 Mostrar solo facturas del cliente logueado
        if cliente:
            self.fields['factura'].queryset = Factura.objects.filter(cliente=cliente)

        # 🔹 Precargar monto si se está seleccionando factura
        if 'factura' in self.data:
            try:
                factura_id = int(self.data.get('factura'))
                factura = Factura.objects.get(pk=factura_id)
                self.fields['monto'].initial = factura.total
            except (ValueError, Factura.DoesNotExist):
                pass
