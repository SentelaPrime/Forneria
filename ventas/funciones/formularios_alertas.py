# ================================================================
# =                                                              =
# =            FORMULARIOS PARA EL SISTEMA DE ALERTAS           =
# =                                                              =
# ================================================================
#
# Este archivo contiene los formularios para crear y editar alertas
# de vencimiento de productos.

from django import forms
from ventas.models import Alertas, Productos


# ================================================================
# =              FORMULARIO: CREAR/EDITAR ALERTA                 =
# ================================================================

class AlertaForm(forms.ModelForm):
    """
    Formulario para crear o editar una alerta manualmente.
    
    Permite al usuario:
    - Seleccionar un producto
    - Elegir el tipo de alerta (verde, amarilla, roja)
    - Escribir un mensaje personalizado
    - Establecer el estado (activa, resuelta, ignorada)
    """
    
    class Meta:
        model = Alertas
        fields = ['productos', 'tipo_alerta', 'mensaje', 'estado']
        
        # --- Etiquetas personalizadas ---
        labels = {
            'productos': 'Producto',
            'tipo_alerta': 'Tipo de alerta',
            'mensaje': 'Mensaje descriptivo',
            'estado': 'Estado de la alerta',
        }
        
        # --- Widgets: Apariencia de los campos ---
        widgets = {
            # Selector de producto (dropdown)
            'productos': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            
            # Selector de tipo de alerta (dropdown)
            'tipo_alerta': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            
            # Campo de texto para el mensaje
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ej: Pan integral vence en 5 días - URGENTE',
                'required': True,
            }),
            
            # Selector de estado
            'estado': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        
        # --- Textos de ayuda ---
        help_texts = {
            'productos': 'Selecciona el producto para esta alerta',
            'tipo_alerta': 'Verde: 30+ días, Amarilla: 14-29 días, Roja: 0-13 días',
            'mensaje': 'Escribe un mensaje descriptivo para la alerta',
            'estado': 'Activa: pendiente, Resuelta: atendida, Ignorada: descartada',
        }
    
    # ============================================================
    # =            PERSONALIZAR QUERYSET DE PRODUCTOS            =
    # ============================================================
    
    def __init__(self, *args, **kwargs):
        """
        Inicializa el formulario y personaliza el selector de productos.
        
        Solo mostramos productos activos (no eliminados) con stock disponible.
        Además, personalizamos cómo se muestra cada producto en el dropdown.
        """
        super().__init__(*args, **kwargs)
        
        # Filtrar solo productos activos con stock
        self.fields['productos'].queryset = Productos.objects.filter(
            eliminado__isnull=True,
            cantidad__gt=0
        ).order_by('nombre')
        
        # Personalizar la presentación de cada producto en el dropdown
        self.fields['productos'].label_from_instance = self.label_producto_personalizado
        
        # Agregar texto placeholder al selector
        self.fields['productos'].empty_label = "-- Seleccionar producto --"
    
    def label_producto_personalizado(self, obj):
        """
        Personaliza cómo se muestra cada producto en el dropdown del formulario.
        
        Formato: "Nombre - Marca (Stock: X, Vence: DD/MM/YYYY)"
        
        Args:
            obj (Productos): Instancia del producto
            
        Returns:
            str: Texto formateado para el dropdown
        
        Ejemplo:
            "Pan Integral - Forneria (Stock: 50, Vence: 25/12/2025)"
        """
        # Comenzar con el nombre del producto
        label = obj.nombre
        
        # Agregar marca si existe
        if obj.marca:
            label += f" - {obj.marca}"
        
        # Agregar información entre paréntesis
        info_extra = []
        
        # Stock disponible
        info_extra.append(f"Stock: {obj.cantidad}")
        
        # Fecha de caducidad
        if obj.caducidad:
            fecha_formateada = obj.caducidad.strftime('%d/%m/%Y')
            info_extra.append(f"Vence: {fecha_formateada}")
        
        # Unir todo
        label += f" ({', '.join(info_extra)})"
        
        return label
    
    # ============================================================
    # =                  VALIDACIONES CUSTOM                     =
    # ============================================================
    
    def clean_mensaje(self):
        """
        Valida y limpia el campo 'mensaje'.
        
        - No puede estar vacío
        - Mínimo 10 caracteres
        - Máximo 255 caracteres
        """
        mensaje = self.cleaned_data.get('mensaje', '').strip()
        
        if not mensaje:
            raise forms.ValidationError("El mensaje no puede estar vacío")
        
        if len(mensaje) < 10:
            raise forms.ValidationError("El mensaje debe tener al menos 10 caracteres")
        
        if len(mensaje) > 255:
            raise forms.ValidationError("El mensaje no puede tener más de 255 caracteres")
        
        return mensaje


# ================================================================
# =           FORMULARIO: FILTROS DE BÚSQUEDA                    =
# ================================================================

class AlertaFiltroForm(forms.Form):
    """
    Formulario para filtrar la lista de alertas.
    
    Permite filtrar por:
    - Tipo de alerta (roja, amarilla, verde)
    - Estado (activa, resuelta, ignorada)
    - Producto (búsqueda por nombre)
    - Rango de fechas
    """
    
    # --- Campo: Tipo de alerta ---
    tipo_alerta = forms.ChoiceField(
        label='Tipo de alerta',
        choices=[
            ('', 'Todos los tipos'),
            ('roja', 'Roja (0-13 días)'),
            ('amarilla', 'Amarilla (14-29 días)'),
            ('verde', 'Verde (30+ días)'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select form-select-sm',
        })
    )
    
    # --- Campo: Estado ---
    estado = forms.ChoiceField(
        label='Estado',
        choices=[
            ('', 'Todos los estados'),
            ('activa', 'Activas'),
            ('resuelta', 'Resueltas'),
            ('ignorada', 'Ignoradas'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select form-select-sm',
        })
    )
    
    # --- Campo: Búsqueda por producto ---
    producto = forms.CharField(
        label='Buscar producto',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': '🔍 Buscar por nombre de producto...',
        })
    )
    
    # --- Campo: Fecha desde ---
    fecha_desde = forms.DateField(
        label='Fecha desde',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control form-control-sm',
            'type': 'date',
        })
    )
    
    # --- Campo: Fecha hasta ---
    fecha_hasta = forms.DateField(
        label='Fecha hasta',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control form-control-sm',
            'type': 'date',
        })
    )
    
    # ============================================================
    # =                  VALIDACIÓN DE FECHAS                    =
    # ============================================================
    
    def clean(self):
        """
        Valida que el rango de fechas sea correcto.
        
        Si se proporciona fecha_desde y fecha_hasta, verificar que
        fecha_desde sea menor o igual a fecha_hasta.
        """
        cleaned_data = super().clean()
        fecha_desde = cleaned_data.get('fecha_desde')
        fecha_hasta = cleaned_data.get('fecha_hasta')
        
        if fecha_desde and fecha_hasta:
            if fecha_desde > fecha_hasta:
                raise forms.ValidationError(
                    "La fecha 'desde' debe ser anterior o igual a la fecha 'hasta'"
                )
        
        return cleaned_data


# ================================================================
# =        FORMULARIO: CAMBIAR ESTADO DE MÚLTIPLES ALERTAS       =
# ================================================================

class CambiarEstadoAlertasForm(forms.Form):
    """
    Formulario para cambiar el estado de múltiples alertas a la vez.
    
    Útil para marcar varias alertas como resueltas o ignoradas
    en una sola acción.
    """
    
    # --- Campo: IDs de las alertas seleccionadas ---
    # Este campo es invisible, se llena con JavaScript
    alertas_ids = forms.CharField(
        widget=forms.HiddenInput(),
        required=True
    )
    
    # --- Campo: Nuevo estado ---
    nuevo_estado = forms.ChoiceField(
        label='Cambiar estado a',
        choices=[
            ('activa', 'Activa'),
            ('resuelta', 'Resuelta'),
            ('ignorada', 'Ignorada'),
        ],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    
    def clean_alertas_ids(self):
        """
        Valida que los IDs sean válidos.
        
        Convierte la cadena de IDs separados por comas en una lista.
        """
        ids_str = self.cleaned_data.get('alertas_ids', '')
        
        if not ids_str:
            raise forms.ValidationError("No se seleccionaron alertas")
        
        try:
            # Convertir "1,2,3" a [1, 2, 3]
            ids_list = [int(id.strip()) for id in ids_str.split(',') if id.strip()]
            
            if not ids_list:
                raise forms.ValidationError("No se seleccionaron alertas válidas")
            
            return ids_list
            
        except ValueError:
            raise forms.ValidationError("IDs de alertas inválidos")

