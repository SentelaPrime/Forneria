from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ventas import views as ventas_views   # IMPORTAR VISTAS DE VENTAS
from forneria import views
from django.contrib.auth import views as auth_views

from ventas.views import (
    productos_por_vencer_api,
    productos_por_vencer_14_dias_api,
    productos_por_vencer_30_dias_api
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página de inicio
    path('', views.home, name='home'),


    # Apps
    path('ventas/', include('ventas.urls')),
    path('rrhh/', include('rrhh.urls')),

    # Login / Logout
    # Logout que cierra sesión y redirige al login automáticamente
    path('accounts/logout/', auth_views.logout_then_login, name='logout'),
    # Registro (signup)
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),

    # APIs de productos próximos a vencer
    path('api/proximos-vencimientos/', productos_por_vencer_api, name='api_proximos_vencimientos'),
    path('api/proximos-vencimientos-14/', productos_por_vencer_14_dias_api, name='api_proximos_vencimientos_14'),
    path('api/proximos-vencimientos-30/', productos_por_vencer_30_dias_api, name='api_proximos_vencimientos_30'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)