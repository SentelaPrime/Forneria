from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from forneria import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('ventas/', include('ventas.urls')),
    path('rrhh/', include('rrhh.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

