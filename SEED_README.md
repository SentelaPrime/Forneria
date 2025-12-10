Instrucciones para cargar la semilla (fixtures) en el proyecto Forneria

Opciones disponibles:

1) Cargar con `loaddata` (recomendado cuando las migraciones están aplicadas)

- Asegúrate de activar el virtualenv y que la base de datos configurada en `forneria/settings.py` esté accesible.
- Ejecuta:

```powershell
& C:\Users\joaqu\forneria\virtual\Scripts\Activate.ps1
python manage.py loaddata ventas/fixtures/initial_data.json
```

Esto insertará las filas definidas para `ventas.producto`, `ventas.venta` y `ventas.detalleventa`.

2) Importar el dump SQL (si prefieres usar el `.sql` que tienes en `Downloads`)

- Si dispones del archivo `forneria (1).sql` y tienes `mysql` en PATH, puedes importarlo desde PowerShell:

```powershell
# Reemplaza usuario y contraseña por tus credenciales locales
mysql -u root -p forneria < "C:\Users\joaqu\Downloads\forneria (1).sql"
```

- Alternativamente puedes abrir phpMyAdmin y ejecutar el SQL allí.

3) Ajuste rápido (si ya tienes el SQL importado o quieres aplicar solo la columna `caducidad`)

- He creado `forneria_modified.sql` en la raíz del proyecto que contiene un `ALTER TABLE` para añadir la columna `caducidad` a `ventas_producto` y un `UPDATE` que establece una fecha de caducidad en el producto con `id=1`.
- Para aplicar solo este cambio (sin reimportar todo el dump), ejecuta:

```powershell
mysql -u root -p forneria < "C:\Users\joaqu\forneria\forneria_modified.sql"
```

Esto permite que las APIs de vencimiento funcionen sin tener que cambiar modelos o migraciones inmediatamente.

Notas y advertencias
- Si tu esquema de base de datos actual no incluye las tablas (o tiene migraciones pendientes), aplica migraciones primero:

```powershell
python manage.py makemigrations
python manage.py migrate
```

- El fixture asume que los modelos `Producto`, `Venta` y `DetalleVenta` ya existen según `ventas/models.py`.
- Si quieres que también se creen usuarios u otros datos de `auth`, puedo generar fixtures adicionales.

¿Quieres que ejecute la carga de la fixture aquí (necesitaría permiso para ejecutar comandos en tu entorno), o prefieres que te guíe por los pasos y verifiques localmente?