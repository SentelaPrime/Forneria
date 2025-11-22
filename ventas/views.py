from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from ventas.models import Producto, Venta, DetalleVenta
from ventas.forms import ProductoForm, VentaForm, DetalleVentaForm

from decimal import Decimal  



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

# NUEVAS VISTAS PARA VENTAS
def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'ventas/lista_ventas.html', {'ventas': ventas})

def nueva_venta(request):
    DetalleFormSet = inlineformset_factory(Venta, DetalleVenta, form=DetalleVentaForm, extra=0, can_delete=True)
    venta_guardada = None

    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.cliente_nombre = request.POST.get('cliente_nombre')
            venta.cliente_rut = request.POST.get('cliente_rut')
            venta.cliente_email = request.POST.get('cliente_email')
            venta.save()

            formset = DetalleFormSet(request.POST, instance=venta, prefix='form')
            if formset.is_valid():
                total = Decimal('0.00')
                for detalle in formset.save(commit=False):
                    if detalle.producto:
                        detalle.precio_unitario = detalle.producto.precio
                        detalle.subtotal = detalle.precio_unitario * detalle.cantidad
                        detalle.save()
                        total += detalle.subtotal

                # ✅ Convertir todo a Decimal para evitar errores float vs Decimal
                descuento = Decimal(venta.descuento or 0)
                iva = Decimal(venta.iva or 0)

                total_desc = total - (total * (descuento / Decimal(100)))
                total_final = total_desc + (total_desc * (iva / Decimal(100)))

                venta.total = total_final.quantize(Decimal('0.01'))  # Redondea a 2 decimales
                venta.save()
                venta_guardada = venta
            else:
                print("❌ Errores en formset:", formset.errors)
    else:
        form = VentaForm()
        formset = DetalleFormSet(prefix='form')

    productos = Producto.objects.all()
    return render(request, 'ventas/formulario_venta.html', {
        'form': form,
        'formset': formset,
        'productos': productos,
        'venta_guardada': venta_guardada,
    })


def generar_factura(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    return render(request, 'ventas/factura.html', {'venta': venta})

@login_required
def index(request):
    return render(request, 'ventas/index.html')
