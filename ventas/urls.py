from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),

    # Productos
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/stock-bajo/', views.stock_bajo, name='stock_bajo'),
    path('productos/nuevo/', views.nuevo_producto, name='nuevo_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

    # Ventas
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/nueva/', views.nueva_venta, name='nueva_venta'),
    path('ventas/factura/<int:venta_id>/', views.generar_factura, name='generar_factura'),
    path('ventas/reporte/', views.ver_reporte, name='ver_reporte'),
    # APIs para productos por vencer
    path('api/productos_por_vencer/7/', views.productos_por_vencer_api, name='productos_por_vencer_7'),
    path('api/productos_por_vencer/14/', views.productos_por_vencer_14_dias_api, name='productos_por_vencer_14'),
    path('api/productos_por_vencer/30/', views.productos_por_vencer_30_dias_api, name='productos_por_vencer_30'),
]
