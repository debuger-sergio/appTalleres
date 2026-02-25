from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

# Modelo que representa la información de la empresa (taller)
class Workshop(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del Taller")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workshops", verbose_name="Dueño")
    logo = models.ImageField(upload_to='workshop_logos/', null=True, blank=True, verbose_name="Logo")
    tax_id = models.CharField(max_length=50, blank=True, verbose_name="CIF/NIF")
    address = models.TextField(blank=True, verbose_name="Dirección")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    email = models.EmailField(blank=True, verbose_name="Email de contacto")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Clase base abstracta para asegurar que todos los datos pertenezcan a un taller específico
class WorkshopBaseModel(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, verbose_name="Taller")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Modelo para gestionar los datos de los clientes
class Client(WorkshopBaseModel):
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellidos")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    dni = models.CharField(max_length=20, blank=True, null=True, verbose_name="DNI/NIE")
    address = models.TextField(blank=True, null=True, verbose_name="Dirección")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Modelo para los vehículos
class Vehicle(WorkshopBaseModel):
    plate = models.CharField(max_length=20, verbose_name="Matrícula")
    brand = models.CharField(max_length=100, verbose_name="Marca")
    model = models.CharField(max_length=100, verbose_name="Modelo")
    year = models.IntegerField(
        null=True, 
        blank=True, 
        validators=[
            MinValueValidator(1900), 
            MaxValueValidator(datetime.date.today().year)
        ], 
        verbose_name="Año"
    )
    vin = models.CharField(max_length=50, blank=True, null=True, verbose_name="Bastidor")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="vehicles", verbose_name="Cliente")

    # Guardamos siempre la matrícula en mayúsculas
    def save(self, *args, **kwargs):
        if self.plate:
            self.plate = self.plate.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.plate} - {self.brand} {self.model}"

# Modelo para las órdenes de trabajo (reparaciones)
class WorkOrder(WorkshopBaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('IN_PROGRESS', 'En Proceso'),
        ('FINISHED', 'Terminado'),
        ('DELIVERED', 'Entregado'),
    ]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="work_orders", verbose_name="Vehículo")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Estado")
    description = models.TextField(verbose_name="Descripción del problema")
    mileage = models.IntegerField(verbose_name="Kilometraje")
    start_date = models.DateField(auto_now_add=True, verbose_name="Fecha de entrada")
    end_date = models.DateField(null=True, blank=True, verbose_name="Fecha de entrega")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)], verbose_name="Importe Total")

    def __str__(self):
        return f"OT {self.id} - {self.vehicle.plate}"

# Líneas de detalle de una orden de trabajo (piezas, mano de obra)
class WorkOrderItem(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=255, verbose_name="Concepto")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1.00, validators=[MinValueValidator(0)], verbose_name="Cantidad")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Precio Unitario")
    
    @property
    def total(self):
        return self.quantity * self.unit_price

# Modelo para presupuestos previos
class Budget(WorkshopBaseModel):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="budgets", verbose_name="Vehículo")
    description = models.TextField(verbose_name="Descripción")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)], verbose_name="Importe Estimado")
    is_approved = models.BooleanField(default=False, verbose_name="¿Aprobado?")

    def __str__(self):
        return f"Presupuesto {self.id} - {self.vehicle.plate}"

# Líneas de detalle de un presupuesto
class BudgetItem(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=255, verbose_name="Concepto")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1.00, validators=[MinValueValidator(0)], verbose_name="Cantidad")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Precio Unitario")

    @property
    def total(self):
        return self.quantity * self.unit_price

# Modelo para facturas generadas a partir de órdenes de trabajo
class Invoice(WorkshopBaseModel):
    order = models.OneToOneField(WorkOrder, on_delete=models.CASCADE, related_name="invoice", verbose_name="Orden de Trabajo")
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name="Número de Factura")
    is_paid = models.BooleanField(default=False, verbose_name="¿Pagada?")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Importe Total")

    def __str__(self):
        return f"Factura {self.invoice_number}"
