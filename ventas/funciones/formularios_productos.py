from django import forms
from django.db.models import Q
from ventas.models.productos import Productos, Categorias, Nutricional
from ventas.funciones.validators import (
    validador_texto_estricto,
    validador_texto_opcional_estricto,
    validador_precio_decimal_estricto,
    validador_entero_no_negativo,
    validador_fecha_no_futuro,
    validador_fecha_no_pasado,
    validador_texto_solo_letras_opcional,
    validador_decimal_opcional_no_negativo,  # NUEVO
)

class ProductoForm(forms.ModelForm):
    # Nuevo: campos auxiliares para construir 'formato'
    formato_cantidad = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={
            'min': '1',
            'step': '1',
            'inputmode': 'numeric',
            'placeholder': 'Ej: 1',
            'pattern': r'^\d+$',
        }),
        label='Formato:'  # etiqueta del grupo
    )
    formato_unidad = forms.ChoiceField(
        required=True,
        choices=[
            ('kg', 'Kilogramos'),
            ('g', 'Gramos'),
            ('l', 'Litros'),
            ('ml', 'Mililitros'),
        ],
        widget=forms.Select(attrs={'title': 'Unidad', 'id': 'id_formato_unidad'}),
        label=''  # sin texto visible para no mostrar "Unidad"
    )

    class Meta:
        model = Productos
        fields = [
            'nombre', 'descripcion', 'marca', 'precio', 'cantidad',
            'caducidad', 'elaboracion', 'tipo',
            'formato', 'categorias'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ej: Pan Integral',
                'autocomplete': 'off',
                'inputmode': 'text',
            }),
            'descripcion': forms.TextInput(attrs={
                'placeholder': 'Ej: Descripción breve',
                'autocomplete': 'off',
                'inputmode': 'text',
            }),
            'marca': forms.TextInput(attrs={
                'placeholder': 'Ej: Fornería',
                'autocomplete': 'off',
                'inputmode': 'text',
            }),
            'tipo': forms.TextInput(attrs={
                'placeholder': 'Ej: Panadería',
                'autocomplete': 'off',
                'inputmode': 'text',
            }),
            'formato': forms.HiddenInput(),  # se completa en save()
            'categorias': forms.Select(attrs={'title': 'Selecciona una categoría'}),
            'caducidad': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'elaboracion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'precio': forms.NumberInput(attrs={
                'min': '0', 'step': '0.01', 'inputmode': 'decimal',
                'placeholder': 'Ej: 1990 o 1990.00',
                'pattern': r'\d{1,8}(\.\d{1,2})?'
            }),
            'cantidad': forms.NumberInput(attrs={
                'min': '0', 'step': '1', 'inputmode': 'numeric',
                'placeholder': 'Ej: 10', 'pattern': r'\d+'
            }),
        }

    def clean_nombre(self):
        return validador_texto_estricto(self.cleaned_data.get('nombre'),
                                        field_label="Nombre del producto", max_len=100)

    def clean_descripcion(self):
        return validador_texto_opcional_estricto(self.cleaned_data.get('descripcion'),
                                                 field_label="Descripción", max_len=300)

    def clean_marca(self):
        # Permite letras, números y espacios; sin signos especiales
        return validador_texto_opcional_estricto(self.cleaned_data.get('marca'),
                                                 field_label="Marca", max_len=100)

    def clean_elaboracion(self):
        # Elaboración opcional: permitir vacío
        valor = self.cleaned_data.get('elaboracion')
        if valor in (None, ''):
            return None
        from ventas.funciones.validators import validador_fecha_no_futuro
        return validador_fecha_no_futuro(valor, field_label="Fecha de elaboración")

    def clean_caducidad(self):
        return validador_fecha_no_pasado(self.cleaned_data.get('caducidad'),
                                         field_label="Fecha de caducidad")

    def clean(self):
        cleaned = super().clean()
        elaboracion = cleaned.get('elaboracion')
        caducidad = cleaned.get('caducidad')
        if elaboracion and caducidad and elaboracion > caducidad:
            self.add_error('caducidad', 'La caducidad debe ser posterior a la fecha de elaboración.')

        # Unicidad por combinación nombre+marca (case-insensitive).
        nombre = cleaned.get('nombre')
        marca = cleaned.get('marca') or None  # el validador opcional puede dejar None/""

        if nombre:
            if not marca:
                # Marca vacía/None: considerar equivalentes NULL y "" en BD
                qs = Productos.objects.filter(
                    nombre__iexact=nombre
                ).filter(Q(marca__isnull=True) | Q(marca__exact=''))
            else:
                qs = Productos.objects.filter(nombre__iexact=nombre, marca__iexact=marca)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                self.add_error('nombre', 'Ya existe un producto con este nombre y marca.')

        return cleaned

    def clean_formato_cantidad(self):
        valor = validador_entero_no_negativo(self.cleaned_data.get('formato_cantidad'),
                                             field_label="Cantidad de formato")
        if int(valor) <= 0:
            raise forms.ValidationError("Debe ser un entero positivo (mayor que 0).")
        return valor

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dejamos "categorias" OPCIONAL como comentaste
        self.fields['categorias'].required = False

        # Mostramos SOLO estas dos opciones en el select
        opciones = ['Perecible', 'No perecible']

        # Buscamos si existen esas categorías en la BD
        qs = Categorias.objects.filter(nombre__in=opciones)

        # Si faltan, las creamos para que el select siempre muestre ambas
        if qs.count() < 2:
            for nombre in opciones:
                # Crea la categoría si no existe (con una descripción simple)
                Categorias.objects.get_or_create(
                    nombre=nombre,
                    defaults={'descripcion': f'Categoria {nombre.lower()}'}
                )
            qs = Categorias.objects.filter(nombre__in=opciones)

        # Asignamos el queryset filtrado y ordenado
        self.fields['categorias'].queryset = qs.order_by('nombre')

        # Quitamos el “---” y usamos un texto claro como placeholder
        self.fields['categorias'].empty_label = "Selecciona categoría..."

        # Prefill de formato al editar (e.g., "1 kg" -> cantidad=1, unidad="kg")
        fmt = getattr(self.instance, 'formato', None)
        if fmt:
            try:
                num, unit = str(fmt).split()
                if num.isdigit():
                    self.fields['formato_cantidad'].initial = int(num)
                unidades_validas = dict(self.fields['formato_unidad'].choices)
                if unit in unidades_validas:
                    self.fields['formato_unidad'].initial = unit
            except Exception:
                pass

    def clean_tipo(self):
        # Validamos “tipo” permitiendo SOLO letras y espacios.
        # Este campo se mantiene OPCIONAL (puede venir vacío).
        return validador_texto_solo_letras_opcional(
            self.cleaned_data.get('tipo'),
            field_label="Tipo",
            max_len=100
        )

    def clean_precio(self):
        from ventas.funciones.validators import validador_precio_decimal_estricto
        return validador_precio_decimal_estricto(self.cleaned_data.get('precio'), field_label="Precio")

    def clean_cantidad(self):
        from ventas.funciones.validators import validador_entero_no_negativo
        return validador_entero_no_negativo(self.cleaned_data.get('cantidad'), field_label="Cantidad")

    def clean_elaboracion(self):
        # Elaboración opcional: permitir vacío
        valor = self.cleaned_data.get('elaboracion')
        if valor in (None, ''):
            return None
        from ventas.funciones.validators import validador_fecha_no_futuro
        return validador_fecha_no_futuro(valor, field_label="Fecha de elaboración")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Prellenar fechas y ajustar formatos de entrada
        self.fields['caducidad'].initial = getattr(self.instance, 'caducidad', None)
        self.fields['elaboracion'].initial = getattr(self.instance, 'elaboracion', None)
        self.fields['caducidad'].input_formats = ['%Y-%m-%d']
        self.fields['elaboracion'].input_formats = ['%Y-%m-%d']

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Completar 'formato' con los campos auxiliares
        cantidad_fmt = self.cleaned_data.get('formato_cantidad')
        unidad_fmt = self.cleaned_data.get('formato_unidad')
        if cantidad_fmt and unidad_fmt:
            instance.formato = f"{cantidad_fmt} {unidad_fmt}"

        # Asegurar que 'nutricional_id' nunca sea NULL
        if instance.nutricional_id is None:
            instance.nutricional = Nutricional.objects.create()

        # Fallback de categoría si no se seleccionó
        if instance.categorias_id is None:
            cat, _ = Categorias.objects.get_or_create(
                nombre='No perecible',
                defaults={'descripcion': 'Categoria no perecible'}
            )
            instance.categorias = cat

        if commit:
            instance.save()
        return instance

class NutricionalForm(forms.ModelForm):
    def clean_calorias(self):
        from ventas.funciones.validators import validador_decimal_opcional_no_negativo
        return validador_decimal_opcional_no_negativo(self.cleaned_data.get('calorias'), "Calorías")

    def clean_proteinas(self):
        from ventas.funciones.validators import validador_decimal_opcional_no_negativo
        return validador_decimal_opcional_no_negativo(self.cleaned_data.get('proteinas'), "Proteínas")

    def clean_grasas(self):
        from ventas.funciones.validators import validador_decimal_opcional_no_negativo
        return validador_decimal_opcional_no_negativo(self.cleaned_data.get('grasas'), "Grasas")

    def clean_carbohidratos(self):
        from ventas.funciones.validators import validador_decimal_opcional_no_negativo
        return validador_decimal_opcional_no_negativo(self.cleaned_data.get('carbohidratos'), "Carbohidratos")

    def clean_azucares(self):
        from ventas.funciones.validators import validador_decimal_opcional_no_negativo
        return validador_decimal_opcional_no_negativo(self.cleaned_data.get('azucares'), "Azúcares")

    def clean_sodio(self):
        from ventas.funciones.validators import validador_decimal_opcional_no_negativo
        return validador_decimal_opcional_no_negativo(self.cleaned_data.get('sodio'), "Sodio")
    class Meta:
        model = Nutricional
        fields = ['calorias', 'proteinas', 'grasas', 'carbohidratos', 'azucares', 'sodio']
        widgets = {
            'calorias': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'placeholder': 'Ej: 250'}),
            'proteinas': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'grasas': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'carbohidratos': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'azucares': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'sodio': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }