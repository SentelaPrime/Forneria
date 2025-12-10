from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from ventas.models import Venta

def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'ventas/lista_ventas.html', {'ventas': ventas})


def generar_factura(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    return render(request, 'ventas/factura.html', {'venta': venta})


@login_required
def home(request):
    return render(request, 'home.html')


def signup(request):
    """Registrar un nuevo usuario usando el formulario estándar de Django.

    Al crear la cuenta, redirige al login y muestra un mensaje.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada correctamente. Por favor inicia sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

