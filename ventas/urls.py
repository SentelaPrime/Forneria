from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),

    # Productos
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/nuevo/', views.nuevo_producto, name='nuevo_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

    # Ventas
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/nueva/', views.nueva_venta, name='nueva_venta'),
    path('ventas/factura/<int:venta_id>/', views.generar_factura, name='generar_factura'),
]
