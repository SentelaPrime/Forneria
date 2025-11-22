from django import forms
from .models import Venta, DetalleVenta, Producto

# CAMBIO AQUÍ: formulario de venta
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['metodo_pago', 'descuento', 'iva']
        widgets = {
            'metodo_pago': forms.Select(attrs={'class': 'form-select'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'iva': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
        }
        labels = {
            'metodo_pago': 'Método de Pago',
            'descuento': 'Descuento (%)',
            'iva': 'IVA (%)',
        }


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar nombre y precio en el select
        self.fields['producto'].queryset = Producto.objects.all()
        self.fields['producto'].label_from_instance = lambda obj: f"{obj.nombre} (${obj.precio})"

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock', 'categoria', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Pan integral artesanal'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Ej: 1200'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Cantidad disponible'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'nombre': 'Nombre del producto',
            'precio': 'Precio ($)',
            'stock': 'Stock disponible',
            'categoria': 'Categoría',
            'imagen': 'Imagen del producto'
        }