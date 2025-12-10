# Validación y Descuento de Stock - Documentación

## Cambios Implementados (10 de diciembre 2025)

### 1. Validación de Stock en DetalleVentaForm
**Archivo:** `ventas/forms.py`

- Agregado método `clean()` en `DetalleVentaForm` que valida:
  - Cantidad solicitada ≤ Stock disponible
  - Si falla: lanza `ValidationError` con mensaje descriptivo
  - El mensaje muestra stock disponible vs. cantidad solicitada

**Cambios en UI:**
- El select de productos ahora muestra: `"Nombre ($precio) - Stock: cantidad"`
- Widget de cantidad tiene atributos: `min="1"`, `class="form-control"`

### 2. Descuento Automático de Stock
**Archivo:** `ventas/views.py` (función `nueva_venta()`)

- Al guardar cada `DetalleVenta`:
  1. Se calcula: `precio_unitario = producto.precio`
  2. Se calcula: `subtotal = precio_unitario * cantidad`
  3. **Se descuenta stock:** `producto.stock -= cantidad`
  4. Se guarda: `producto.save()`

**Flujo completo:**
```
usuario crea venta → valida stock en form → guarda detalles → descuenta stock → guarda producto
```

### 3. Manejo de Errores

Si el usuario intenta vender más de lo disponible:
- **En formulario:** Mensaje de validación antes de guardar
- **Descuento:** Solo ocurre si la venta se guarda exitosamente

### 4. Ejemplo de Uso

1. Usuario accede a `/ventas/nueva_venta/`
2. Selecciona producto: "Pan integral ($500) - Stock: 10"
3. Intenta vender cantidad: 15
4. Formulario muestra error: "Stock insuficiente. Disponible: 10. Solicitado: 15"
5. Si cambia a 8 unidades y confirma:
   - Stock de "Pan integral" pasa de 10 a 2
   - Se crea venta con 8 unidades

## Notas Técnicas

- **Sin cambios en modelos:** Solo cambios en forms.py y views.py
- **Transacciones:** Django maneja automáticamente; si hay error, no se guarda nada
- **Productos:** Stock nunca será negativo si validación funciona correctamente
- **Detalles eliminados:** Si usuario borra items del formset, **no se recupera stock** (diseño actual)

## Posibles Mejoras Futuras

1. Recuperar stock si usuario cancela o elimina detalles
2. Historial de movimientos de stock (auditoría)
3. Alertas de reorden automático
4. Reserva de stock antes de confirmar venta
