import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forneria.settings')
import django
django.setup()
from ventas.models import Venta
print('Ventas en DB:', Venta.objects.count())
