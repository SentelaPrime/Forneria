from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ventas import views as ventas_views   # IMPORTAR VISTAS DE VENTAS
from forneria import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página de inicio
    path('', views.home, name='home'),


    # Apps
    path('ventas/', include('ventas.urls')),
    path('rrhh/', include('rrhh.urls')),

    # Login / Logout
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)