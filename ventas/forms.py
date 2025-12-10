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
        widgets = {
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Cantidad'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar nombre y precio en el select
        self.fields['producto'].queryset = Producto.objects.all()
        self.fields['producto'].label_from_instance = lambda obj: f"{obj.nombre} (${obj.precio}) - Stock: {obj.stock}"

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')
        
        if producto and cantidad:
            if cantidad > producto.stock:
                raise forms.ValidationError(
                    f"Stock insuficiente. Disponible: {producto.stock} unidades. Solicitado: {cantidad}"
                )
        
        return cleaned_data

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock', 'categoria', 'imagen', 'caducidad']
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
            'caducidad': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'nombre': 'Nombre del producto',
            'precio': 'Precio ($)',
            'stock': 'Stock disponible',
            'categoria': 'Categoría',
            'imagen': 'Imagen del producto'
            , 'caducidad': 'Fecha de caducidad'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si se está creando (no existe pk), hacer caducidad requerida
        if not (self.instance and self.instance.pk):
            self.fields['caducidad'].required = True
            self.fields['caducidad'].widget.attrs.update({'required': 'required'})