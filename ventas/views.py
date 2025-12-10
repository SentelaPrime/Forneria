from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from ventas.models import Producto, Venta, DetalleVenta
from ventas.forms import ProductoForm, VentaForm, DetalleVentaForm

from django.http import JsonResponse
from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Sum

from decimal import Decimal  


# --- API: productos por vencer en los próximos X días ---
def _productos_por_vencer(dias):
    hoy = date.today()
    limite = hoy + timedelta(days=dias)
    # Si el modelo Producto no tiene el campo `caducidad`, devolver lista vacía
    try:
        Producto._meta.get_field('caducidad')
    except Exception:
        return []

    productos = Producto.objects.filter(caducidad__range=(hoy, limite)).order_by('caducidad')

    return [
        {
            "nombre": p.nombre,
            "caducidad": p.caducidad.strftime("%Y-%m-%d")
        }
        for p in productos
    ]


def productos_por_vencer_api(request):
    return JsonResponse({"items": _productos_por_vencer(7)})


def productos_por_vencer_14_dias_api(request):
    return JsonResponse({"items": _productos_por_vencer(14)})


def productos_por_vencer_30_dias_api(request):
    return JsonResponse({"items": _productos_por_vencer(30)})



# VISTA EXISTENTE DE PRODUCTOS (sin cambios)
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista.html', {'productos': productos})

# VISTA EXISTENTE DE PRODUCTOS (sin cambios)
def nuevo_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ventas:lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/formulario.html', {'form': form})

def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST,request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('ventas:lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/formulario.html', {'form': form})

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('ventas:lista_productos')
    return render(request, 'productos/confirmar_eliminar.html', {'producto': producto})


# DATOS DE VENTA
def ver_reporte(request):
    # Métricas para el dashboard de reportes
    today = timezone.localdate()
    ventas_hoy = Venta.objects.filter(fecha__date=today).count()

    # Stock bajo: productos con stock menor o igual a 5 (umbral configurable)
    STOCK_BAJO_UMBRAL = 5
    stock_bajo_count = Producto.objects.filter(stock__lte=STOCK_BAJO_UMBRAL).count()

    # Top producto por unidades vendidas (sum cantidad en DetalleVenta)
    top = (
        DetalleVenta.objects.values('producto__nombre')
        .annotate(unidades=Sum('cantidad'))
        .order_by('-unidades')
        .first()
    )
    if top:
        top_producto = {'nombre': top['producto__nombre'], 'unidades': top['unidades']}
    else:
        top_producto = None

    context = {
        'ventas_hoy': ventas_hoy,
        'stock_bajo_count': stock_bajo_count,
        'top_producto': top_producto,
    }
    return render(request, 'ventas/reporte.html', context)


def stock_bajo(request):
    """Lista de productos con stock bajo (umbral 5). Reutiliza la plantilla de lista de productos."""
    STOCK_BAJO_UMBRAL = 5
    productos = Producto.objects.filter(stock__lte=STOCK_BAJO_UMBRAL).order_by('stock')
    return render(request, 'productos/lista.html', {'productos': productos})

# NUEVAS VISTAS PARA VENTAS
def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'ventas/lista_ventas.html', {'ventas': ventas})

def nueva_venta(request):
    DetalleFormSet = inlineformset_factory(Venta, DetalleVenta, form=DetalleVentaForm, extra=0, can_delete=True)
    venta_guardada = None
    formset_errors = []
    cliente_errors = []
    form = None
    formset = None

    if request.method == 'POST':
        # VALIDAR DATOS DEL CLIENTE
        cliente_nombre = request.POST.get('cliente_nombre', '').strip()
        cliente_email = request.POST.get('cliente_email', '').strip()
        cliente_rut = request.POST.get('cliente_rut', '').strip()
        
        if not cliente_nombre:
            cliente_errors.append("El nombre del cliente es obligatorio.")
        if not cliente_email:
            cliente_errors.append("El correo del cliente es obligatorio.")
        if not cliente_rut:
            cliente_errors.append("El RUT/DNI del cliente es obligatorio.")
        
        if cliente_errors:
            form = VentaForm(request.POST)
            formset = DetalleFormSet(request.POST, prefix='form')
        else:
            form = VentaForm(request.POST)
            if form.is_valid():
                venta = form.save(commit=False)
                venta.cliente_nombre = cliente_nombre
                venta.cliente_rut = cliente_rut
                venta.cliente_email = cliente_email
                venta.save()

                formset = DetalleFormSet(request.POST, instance=venta, prefix='form')
                if formset.is_valid():
                    # VALIDAR STOCK ANTES DE GUARDAR
                    detalles_a_guardar = []
                    for idx, detalle in enumerate(formset.save(commit=False)):
                        if detalle.producto:
                            # Verificar que el stock sea suficiente
                            if detalle.cantidad > detalle.producto.stock:
                                formset_errors.append(
                                    f"Línea {idx + 1}: Stock insuficiente para '{detalle.producto.nombre}'. "
                                    f"Disponible: {detalle.producto.stock}, Solicitado: {detalle.cantidad}"
                                )
                                venta.delete()  # Eliminar venta si hay error
                                break
                            detalles_a_guardar.append(detalle)
                    
                    if not formset_errors:
                        # Si no hay errores, proceder a guardar y descontar stock
                        total = Decimal('0.00')
                        for detalle in detalles_a_guardar:
                            detalle.precio_unitario = detalle.producto.precio
                            detalle.subtotal = detalle.precio_unitario * detalle.cantidad
                            detalle.save()
                            total += detalle.subtotal
                            
                            # DESCUENTO DE STOCK: restar cantidad del producto
                            detalle.producto.stock -= detalle.cantidad
                            detalle.producto.save()

                        # Convertir todo a Decimal para evitar errores float vs Decimal
                        descuento = Decimal(venta.descuento or 0)
                        iva = Decimal(venta.iva or 0)

                        total_desc = total - (total * (descuento / Decimal(100)))
                        total_final = total_desc + (total_desc * (iva / Decimal(100)))

                        venta.total = total_final.quantize(Decimal('0.01'))  # Redondea a 2 decimales
                        venta.save()
                        venta_guardada = venta
                else:
                    formset_errors = list(formset.non_form_errors())
                    for form_errors in formset.errors:
                        for error in form_errors.values():
                            formset_errors.extend(error)
                    venta.delete()  # Eliminar venta si hay errores en formset
            else:
                formset = DetalleFormSet(request.POST, prefix='form')
    else:
        form = VentaForm()
        formset = DetalleFormSet(prefix='form')

    productos = Producto.objects.all()
    return render(request, 'ventas/formulario_venta.html', {
        'form': form,
        'formset': formset,
        'productos': productos,
        'venta_guardada': venta_guardada,
        'formset_errors': formset_errors,
        'cliente_errors': cliente_errors,
    })


def generar_factura(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    return render(request, 'ventas/factura.html', {'venta': venta})

@login_required
def index(request):
    return render(request, 'ventas/index.html')
