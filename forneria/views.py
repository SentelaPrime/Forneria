from django.shortcuts import render
from django.contrib.auth.decorators import login_required
def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'ventas/lista_ventas.html', {'ventas': ventas})
def generar_factura(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    return render(request, 'ventas/factura.html', {'venta': venta})
@login_required
def home(request):
    return render(request, 'home.html')

