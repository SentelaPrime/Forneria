from django.db import models

class Producto(models.Model):
    CATEGORIAS = [
        ('pan', 'Panadería'),
        ('pastel', 'Pastelería'),
        ('bebida', 'Bebidas'),
        ('otros', 'Otros'),
    ]

    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='otros')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # 👈 clave aquí

    def __str__(self):
        return self.nombre


# CAMBIO AQUÍ: modificar Venta para metodo_pago y total
class Venta(models.Model):
    METODOS_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
        ('Transferencia', 'Transferencia'),
    ]
    fecha = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default='Efectivo')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # en porcentaje
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=0)        # en porcentaje

    cliente_nombre = models.CharField(max_length=100)
    cliente_rut = models.CharField(max_length=20, blank=True, null=True)
    cliente_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha.strftime('%d/%m/%Y')}"

# CAMBIO AQUÍ: nuevo modelo DetalleVenta
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.precio_unitario * self.cantidad
        super().save(*args, **kwargs)
