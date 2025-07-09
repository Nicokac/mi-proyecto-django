# ordenes_compra/forms.py
from django import forms
from .models import OrdenDeCompra, DetalleOrden
from proveedores.models import Proveedor
from productos.models import Producto
from django.forms import inlineformset_factory

class OrdenDeCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenDeCompra
        fields = ['proveedor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Excluir "Cafe El Mejor"
        self.fields['proveedor'].queryset = Proveedor.objects.exclude(nombre__iexact="Cafe El Mejor")

        # Que sea obligatorio solo para admin
        self.fields['proveedor'].required = False

class DetalleOrdenForm(forms.ModelForm):
    class Meta:
        model = DetalleOrden
        fields = ['producto', 'cantidad']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_staff:
            proveedor_cafe = Proveedor.objects.get(nombre__iexact="Cafe El Mejor")
            self.fields['producto'].queryset = Producto.objects.filter(estado=True, proveedor=proveedor_cafe)
        else:
            self.fields['producto'].queryset = Producto.objects.filter(estado=True)

# ✅ Con esto permitimos eliminar detalles vacíos o no deseados
DetalleOrdenFormSet = inlineformset_factory(
    OrdenDeCompra,
    DetalleOrden,
    form=DetalleOrdenForm,
    extra=1,
    can_delete=True
)
