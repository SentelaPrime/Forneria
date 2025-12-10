# ================================================================
# =                                                              =
# =          FORMULARIOS PARA EL SISTEMA DE VENTAS              =
# =                                                              =
# ================================================================
# 
# Este archivo contiene los formularios (forms) que se usan para
# capturar información de clientes y ventas en la Forneria.
# 
# Los formularios en Django son como "plantillas de validación" que:
# 1. Definen qué información necesitamos del usuario
# 2. Validan que esa información sea correcta
# 3. Muestran errores si algo está mal
# 4. Guardan los datos en la base de datos

from django import forms
from ventas.models import Clientes, Ventas
from .validators import sanitizador_texto


# ================================================================
# =              FORMULARIO: CLIENTE RÁPIDO                      =
# ================================================================
# 
# Este formulario se usa para registrar clientes de forma rápida
# durante una venta. Solo pide el nombre (obligatorio) y
# opcionalmente el RUT y correo.

class ClienteRapidoForm(forms.ModelForm):
    """
    Formulario para agregar un cliente rápidamente.
    
    - Solo el nombre es obligatorio
    - RUT y correo son opcionales
    - Se usa en el punto de venta (POS) cuando se necesita
      registrar un cliente nuevo mientras se hace una venta
    """
    
    # --- Configuración del formulario ---
    class Meta:
        # Le decimos a Django que este formulario está basado en el modelo Clientes
        model = Clientes
        
        # Indicamos qué campos del modelo queremos incluir en el formulario
        fields = ['nombre', 'rut', 'correo']
        
        # --- Etiquetas personalizadas ---
        # Son los textos que aparecen sobre cada campo en el formulario
        labels = {
            'nombre': 'Nombre del cliente',  # En lugar de solo "Nombre"
            'rut': 'RUT (opcional)',         # Dejamos claro que es opcional
            'correo': 'Correo (opcional)',   # Dejamos claro que es opcional
        }
        
        # --- Widgets: Cómo se ven los campos en HTML ---
        # Aquí configuramos el aspecto visual de cada campo
        widgets = {
            # Campo de nombre: es un cuadro de texto normal
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',           # Clase CSS de Bootstrap para estilo
                'placeholder': 'Ej: Juan Pérez',   # Texto de ayuda dentro del campo
                'autocomplete': 'name',            # Ayuda a los navegadores a autocompletar
                'required': True,                  # HTML5: campo obligatorio
            }),
            
            # Campo de RUT: cuadro de texto con formato especial
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12.345.678-9', # Ejemplo del formato chileno
                'autocomplete': 'off',             # No autocompletar (por privacidad)
            }),
            
            # Campo de correo: cuadro especializado para emails
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'cliente@ejemplo.com',
                'autocomplete': 'email',           # Ayuda a autocompletar el email
            }),
        }
        
        # --- Textos de ayuda ---
        # Pequeñas instrucciones que aparecen debajo de cada campo
        help_texts = {
            'nombre': 'Nombre completo del cliente',
            'rut': 'RUT chileno con formato 12.345.678-9 (opcional)',
            'correo': 'Email para enviar boleta electrónica (opcional)',
        }
    
    # ============================================================
    # =            VALIDACIONES PERSONALIZADAS                   =
    # ============================================================
    
    def clean_nombre(self):
        """
        Valida y limpia el campo 'nombre'.
        
        Pasos:
        1. Obtiene el valor que el usuario escribió
        2. Limpia espacios extra y caracteres peligrosos
        3. Verifica que no esté vacío
        4. Retorna el nombre limpio
        
        Si algo falla, Django mostrará un error automáticamente.
        """
        # Obtenemos el nombre que el usuario escribió
        nombre_original = self.cleaned_data.get('nombre')
        
        # Lo limpiamos con nuestra función sanitizadora
        # (quita espacios extra, caracteres raros, etc.)
        nombre_limpio = sanitizador_texto(nombre_original)
        
        # Verificamos que después de limpiar, todavía haya algo
        if not nombre_limpio:
            # Si está vacío, lanzamos un error
            raise forms.ValidationError("El nombre del cliente es obligatorio")
        
        # Si todo está bien, retornamos el nombre limpio
        return nombre_limpio
    
    def clean_rut(self):
        """
        Valida y limpia el campo 'rut'.
        
        El RUT es opcional, pero si lo proporcionan, debe:
        - Estar en formato correcto (12.345.678-9)
        - No tener caracteres extraños
        """
        rut_original = self.cleaned_data.get('rut')
        
        # Si no hay RUT (es opcional), no hay nada que validar
        if not rut_original:
            return ''  # Retornamos cadena vacía
        
        # Limpiamos el RUT
        rut_limpio = sanitizador_texto(rut_original)
        
        # TODO: Aquí podrías agregar validación del dígito verificador
        # Por ahora solo limpiamos caracteres peligrosos
        
        return rut_limpio
    
    def clean_correo(self):
        """
        Valida y limpia el campo 'correo'.
        
        El correo es opcional, pero si lo proporcionan,
        Django ya verifica que tenga formato válido (con @, dominio, etc.)
        porque usamos EmailField en el modelo.
        """
        correo_original = self.cleaned_data.get('correo')
        
        # Si no hay correo (es opcional), retornamos vacío
        if not correo_original:
            return ''
        
        # Django ya validó el formato, solo limpiamos y convertimos a minúsculas
        correo_limpio = correo_original.strip().lower()
        
        return correo_limpio


# ================================================================
# =         FORMULARIO: SELECCIONAR CLIENTE EXISTENTE            =
# ================================================================
# 
# Este formulario se usa cuando queremos seleccionar un cliente
# que ya está registrado en el sistema.

class SeleccionarClienteForm(forms.Form):
    """
    Formulario simple para seleccionar un cliente existente
    desde un dropdown (lista desplegable).
    """
    
    # --- Campo: Cliente ---
    # Este es un campo que mostrará una lista desplegable con todos los clientes
    cliente = forms.ModelChoiceField(
        # Traemos todos los clientes de la base de datos, ordenados alfabéticamente
        queryset=Clientes.objects.all().order_by('nombre'),
        
        # Texto que aparece cuando no hay nada seleccionado
        empty_label="-- Seleccionar cliente --",
        
        # Es obligatorio seleccionar uno
        required=False,
        
        # Texto que aparece sobre el campo
        label="Cliente",
        
        # Cómo se ve el campo (dropdown con estilo Bootstrap)
        widget=forms.Select(attrs={
            'class': 'form-select',      # Clase CSS de Bootstrap 5
            'id': 'id_cliente_select',   # ID único para JavaScript
        })
    )


# ================================================================
# =              FORMULARIO: FINALIZAR VENTA                     =
# ================================================================
# 
# Este formulario se usa al momento de finalizar una venta
# para capturar información adicional como el método de pago,
# el monto pagado, etc.

class FinalizarVentaForm(forms.Form):
    """
    Formulario para capturar datos finales de la venta:
    - Canal de venta (presencial o delivery)
    - Monto pagado por el cliente
    - Si quiere factura o boleta
    """
    
    # --- Campo: Canal de venta ---
    # ¿La venta es presencial o por delivery?
    canal_venta = forms.ChoiceField(
        choices=[
            ('presencial', 'Presencial'),
            ('delivery', 'Delivery'),
        ],
        initial='presencial',   # Por defecto está en 'presencial'
        required=True,
        label='Canal de venta',
        widget=forms.RadioSelect(attrs={  # Botones de radio (círculos seleccionables)
            'class': 'form-check-input'
        })
    )
    
    # --- Campo: Monto pagado ---
    # Cuánto dinero entregó el cliente
    monto_pagado = forms.DecimalField(
        max_digits=10,           # Hasta 10 dígitos en total
        decimal_places=2,        # 2 decimales (ej: 1234.56)
        required=True,
        label='Monto pagado por el cliente',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01',      # Permite decimales en el input HTML5
            'min': '0',          # No puede ser negativo
        })
    )
    
    # --- Campo: Descuento (opcional) ---
    # Si queremos aplicar un descuento global a la venta
    descuento = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,          # Es opcional
        initial=0,               # Por defecto, sin descuento
        label='Descuento (opcional)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01',
            'min': '0',
        })
    )
    
    # ============================================================
    # =            VALIDACIÓN: MONTO PAGADO                      =
    # ============================================================
    
    def clean_monto_pagado(self):
        """
        Valida que el monto pagado sea un número positivo.
        """
        monto = self.cleaned_data.get('monto_pagado')
        
        if monto is None:
            raise forms.ValidationError("Debe ingresar el monto pagado")
        
        if monto < 0:
            raise forms.ValidationError("El monto no puede ser negativo")
        
        return monto
    
    def clean_descuento(self):
        """
        Valida que el descuento (si se proporciona) sea válido.
        """
        descuento = self.cleaned_data.get('descuento')
        
        # Si no hay descuento, retornamos 0
        if descuento is None:
            return 0
        
        if descuento < 0:
            raise forms.ValidationError("El descuento no puede ser negativo")
        
        return descuento

