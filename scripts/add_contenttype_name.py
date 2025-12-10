import os
import django
from django.db import connection
import sys

# Añadir el proyecto al path para importar settings
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forneria.settings')
django.setup()

with connection.cursor() as cursor:
    # Comprobar si existe la columna 'name' en django_content_type
    cursor.execute("SHOW COLUMNS FROM django_content_type LIKE 'name';")
    result = cursor.fetchone()
    if result:
        print("La columna 'name' ya existe en django_content_type.")
    else:
        print("Columna 'name' no encontrada. Añadiéndola...")
        try:
            cursor.execute("ALTER TABLE django_content_type ADD COLUMN `name` varchar(255) NULL;")
            print("Columna 'name' añadida correctamente.")
        except Exception as e:
            print("Error al añadir la columna:", e)
