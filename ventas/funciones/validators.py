import re
from django.core.exceptions import ValidationError

# Aquí definimos una función que acepta un parámetro value 
# que será el texto que queremos limpiar.
def sanitizador_texto(value):
    """
    Limpia un texto eliminando epacios extra al inicio, medio y final
    """
    if value is None:
        return None # Si no hay valor no hacemo nada

    # elimina espacion al final y inicio
    value_strip = value.strip()

    # divide el texto por los espacios y vuelve a unirlo con un solo espacio
    value_sin_espacios = ' '.join(value_strip.split())
    
    return value_sin_espacios

def validador_nombre(value, field_label="Nombre"):
    """
    No puede estar vacío.
    No puede contener caracteres de HTML ('<' o '>').
    Permite letras (incluyendo acentos), espacios, apóstrofos y guiones.
    Debe tener entre 2 y 100 caracteres.
    """ 

    # Limpiamos el texto de espacios extra
    value = sanitizador_texto(value)

    # Revismos que no este vacio
    if not value:
        raise ValidationError(f"{field_label} no puede estar vacío.")

    # Revisamos que no tenga codigo de html
    if "<" in value or ">" in value:
        raise ValidationError(f"Caracteres no permitidos en {field_label}.")

   # filtramos caracteres  y la longitud
    if not re.fullmatch(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s'-]{2,100}$", value):
        raise ValidationError(f"{field_label} solo puede contener letras, maximo 100 caracteres")

    # si todo esta bien devolvemos con el return
    return value

def validador_correo(value):
    """
    Valida el campo de correo:
    No puede star vacio
    No puede contenet caracteres de html <>
    Debe tener un formato valido usuario@dominio.com
    Hacer que este en minuscula
    """    
    # limpiar espacios extra
    valor_limpio = sanitizador_texto(value)

    # verificar que no este vacio
    if not valor_limpio:
        raise ValidationError("El correo no puede estar vacío.")

    # Bloquear intentos de html/xss
    if "<" in valor_limpio or ">" in valor_limpio:
        raise ValidationError("Caracteres no permitidos en el correo.")

    # Validar el patron estandar de email
    patron_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.fullmatch(patron_email, valor_limpio):
        raise ValidationError("Formato de correo electrónico inválido.")
    
    # devolver en minusculas
    correo_minuscula = valor_limpio.lower()
    return correo_minuscula

def validador_usuario(value):
    """
    Valida nombre de usuario
    No puede estar vacio
    No puede contener caracteres de html/xss
    Caracteres permitidos . _ -
    longitud maximo 50
    """
    # Limpiamos el texto de espacios extra
    value = sanitizador_texto(value)

    # Revismos que no este vacio
    if not value:
        raise ValidationError("El nombre de usuario no puede estar vacío.")

    # Revisamos que no tenga codigo de html
    if "<" in value or ">" in value:
        raise ValidationError("Caracteres no permitidos en el nombre de usuario.")

    # filtramos caracteres  y la longitud
    if not re.fullmatch(r"^[a-zA-Z0-9._-]{2,50}$", value):
        raise ValidationError("El nombre de usuario solo puede contener letras, números, puntos, guiones y guiones bajos, y debe tener entre 2 y 50 caracteres.")

    # si todo esta bien devolvemos con el return
    return value

def validador_contrasena_login(value):
    """
    Valida contraseña para LOGIN:
    - Obligatoria.
    - No espacios.
    - No caracteres de HTML '<' o '>'.
    - No se modifica el valor (no se aplican 'strip' ni sanitización).
    """
    if value is None or value == "":
        raise ValidationError("La contraseña es requerida.")

    if "<" in value or ">" in value:
        raise ValidationError("Caracteres no permitidos en la contraseña.")

    if " " in value:
        raise ValidationError("La contraseña no debe contener espacios.")

    return value

def validador_contrasena_registro(value):
    """
    Valida contraseña para REGISTRO:
    - Obligatoria.
    - Mínimo 8 caracteres.
    - Debe incluir letras y números.
    - Sin espacios y sin '<' o '>'.
    - Permite símbolos seguros: @#$%^&*()_-+=.!?;:,
    """
    if value is None or value == "":
        raise ValidationError("La contraseña es requerida.")

    if "<" in value or ">" in value:
        raise ValidationError("Caracteres no permitidos en la contraseña.")

    if " " in value:
        raise ValidationError("La contraseña no debe contener espacios.")

    if len(value) < 8:
        raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

    if not re.search(r"[A-Za-z]", value):
        raise ValidationError("La contraseña debe incluir letras.")

    if not re.search(r"[0-9]", value):
        raise ValidationError("La contraseña debe incluir números.")

    # Restringimos a un conjunto de símbolos comunes y seguros.
    if not re.fullmatch(r"[A-Za-z0-9@#$%^&*()_\-+=.!?;:,]{8,128}", value):
        raise ValidationError("La contraseña contiene caracteres no permitidos.")

    return value

# Funciones estrictas para productos (precio y textos)
from decimal import Decimal, InvalidOperation
import re
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

def validador_precio_decimal_estricto(value, field_label="Precio"):
    """
    Solo dígitos y punto con hasta 2 decimales. Debe ser > 0. Sin letras/símbolos.
    """
    if value is None or value == "":
        raise ValidationError(f"{field_label} es requerido.")
    if not re.fullmatch(r"^\d{1,8}(\.\d{1,2})?$", str(value)):
        raise ValidationError(f"{field_label} debe ser numérico con hasta 2 decimales. Solo dígitos y punto.")
    try:
        dec = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValidationError(f"{field_label} inválido.")
    if dec <= 0:
        raise ValidationError(f"{field_label} debe ser mayor que 0.")
    return dec

def validador_entero_no_negativo(value, field_label="Valor"):
    """
    Entero requerido y no negativo. Solo dígitos.
    """
    if value is None or value == "":
        raise ValidationError(f"{field_label} es requerido.")
    if not re.fullmatch(r"^\d+$", str(value)):
        raise ValidationError(f"{field_label} debe ser un entero (solo dígitos).")
    ivalue = int(value)
    if ivalue < 0:
        raise ValidationError(f"{field_label} no puede ser negativo.")
    return ivalue

def validador_texto_estricto(value, field_label="Texto", max_len=100):
    v = sanitizador_texto(value)
    if not v:
        raise ValidationError(f"{field_label} no puede estar vacío.")
    if "<" in v or ">" in v:
        raise ValidationError(f"Caracteres no permitidos en {field_label}.")
    patron = rf"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]{{1,{max_len}}}$"
    if not re.fullmatch(patron, v):
        raise ValidationError(f"{field_label} solo permite letras, números y espacios. Máximo {max_len} caracteres.")
    return v

def validador_texto_opcional_estricto(value, field_label="Texto", max_len=100):
    v = sanitizador_texto(value)
    if v in (None, ""):
        return None
    if "<" in v or ">" in v:
        raise ValidationError(f"Caracteres no permitidos en {field_label}.")
    patron = rf"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]{{1,{max_len}}}$"
    if not re.fullmatch(patron, v):
        raise ValidationError(f"{field_label} solo permite letras, números y espacios. Máximo {max_len} caracteres.")
    return v

def validador_fecha_no_futuro(value, field_label="Fecha"):
    """
    Acepta objetos date o 'YYYY-MM-DD'. No puede ser mayor que la fecha actual.
    """
    if value is None or value == "":
        raise ValidationError(f"{field_label} es requerida.")
    day = value if isinstance(value, date) else None
    if day is None:
        try:
            day = date.fromisoformat(str(value))
        except Exception:
            raise ValidationError(f"{field_label} inválida.")
    hoy = timezone.localdate()
    if day > hoy:
        raise ValidationError(f"{field_label} no puede ser posterior a hoy.")
    return day

def validador_fecha_no_pasado(value, field_label="Fecha"):
    """
    Acepta objetos date o 'YYYY-MM-DD'. No puede ser menor que la fecha actual.
    """
    if value is None or value == "":
        raise ValidationError(f"{field_label} es requerida.")
    day = value if isinstance(value, date) else None
    if day is None:
        try:
            day = date.fromisoformat(str(value))
        except Exception:
            raise ValidationError(f"{field_label} inválida.")
    hoy = timezone.localdate()
    if day < hoy:
        raise ValidationError(f"{field_label} no puede ser anterior a hoy.")
    return day

def validador_texto_solo_letras_opcional(value, field_label="Texto", max_len=100):
    """
    Versión OPCIONAL de texto solo letras y espacios.
    - Permite vacío (None o "").
    - Bloquea caracteres de HTML.
    - Acepta acentos y Ñ.
    """
    # Normalizamos espacios (inicio/medio/final)
    v = sanitizador_texto(value)

    # Si viene vacío, devolvemos vacío
    if v in (None, ""):
        return None

    # Bloquear intentos de HTML/XSS
    if "<" in v or ">" in v:
        raise ValidationError(f"Caracteres no permitidos en {field_label}.")

    # Solo letras y espacios, con acentos y Ñ, con longitud máxima
    patron = rf"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]{{1,{max_len}}}$"
    if not re.fullmatch(patron, v):
        raise ValidationError(f"{field_label} solo permite letras y espacios. Máximo {max_len} caracteres.")

    # Si todo está bien, devolvemos el valor limpio
    return v


def validador_texto_solo_letras(value, field_label="Texto", max_len=100, allow_empty=False):
    """
    Valida texto SOLO letras y espacios.
    - Si allow_empty=True, permite vacío (None o "").
    - Bloquea intentos de HTML ('<' y '>').
    - Acepta acentos y la Ñ.
    """
    # Normalizamos espacios extra (inicio/medio/final)
    v = sanitizador_texto(value)

    # Si viene vacío y NO se permite vacío, mostramos error
    if not v and not allow_empty:
        raise ValidationError(f"{field_label} no puede estar vacío.")

    # Si está vacío y sí se permite, devolvemos None (campo opcional)
    if v in (None, ""):
        return None

    # Bloqueamos intentos de HTML/XSS
    if "<" in v or ">" in v:
        raise ValidationError(f"Caracteres no permitidos en {field_label}.")

    # Solo letras y espacios (con acentos y Ñ), con longitud máxima
    patron = rf"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]{{1,{max_len}}}$"
    if not re.fullmatch(patron, v):
        raise ValidationError(f"{field_label} solo permite letras y espacios. Máximo {max_len} caracteres.")

    # Si todo está bien, devolvemos el valor ya limpio
    return v


def validador_decimal_opcional_no_negativo(value, field_label="Valor"):
    """
    Opcional: permite None/"".
    Solo dígitos y punto, hasta 2 decimales. No negativos.
    """
    if value in (None, ""):
        return None
    if not re.fullmatch(r"^\d{1,8}(\.\d{1,2})?$", str(value)):
        raise ValidationError(f"{field_label} debe ser numérico con hasta 2 decimales. Solo dígitos y punto.")
    try:
        dec = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValidationError(f"{field_label} inválido.")
    if dec < 0:
        raise ValidationError(f"{field_label} no puede ser negativo.")
    return dec
