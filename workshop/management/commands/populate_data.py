from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from workshop.models import Workshop, Client, Vehicle, WorkOrder, Budget
import random

# Comando de gestión para poblar la base de datos con datos de ejemplo
class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Poblando base de datos...")

        # 1. Obtener o crear el usuario administrador por defecto
        admin_user = User.objects.filter(username='admin').first()
        if not admin_user:
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS("Usuario 'admin' creado."))

        # 2. Crear un Taller de ejemplo vinculado al administrador
        workshop, created = Workshop.objects.get_or_create(
            owner=admin_user,
            defaults={
                'name': 'Talleres Sevilla Motor',
                'tax_id': 'B-12345678',
                'address': 'Polígono Calonge, Sevilla',
                'phone': '954000111',
                'email': 'contacto@sevillamotor.com'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Taller '{workshop.name}' creado."))

        # 3. Crear Clientes de ejemplo
        clients_data = [
            ('Juan', 'García', '600111222', 'juan@email.com'),
            ('María', 'Pérez', '611222333', 'maria@email.com'),
            ('Antonio', 'Jiménez', '622333444', None),
            ('Lucía', 'Fernández', '633444555', 'lucia@email.com'),
        ]

        clients = []
        for first_name, last_name, phone, email in clients_data:
            c, created = Client.objects.get_or_create(
                workshop=workshop,
                phone=phone,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                }
            )
            clients.append(c)
            if created:
                self.stdout.write(f"Cliente {first_name} creado.")

        # 4. Crear Vehículos de ejemplo vinculados a los clientes
        vehicles_data = [
            ('1234ABC', 'Toyota', 'Corolla', 2018, clients[0]),
            ('5678DEF', 'Seat', 'Ibiza', 2020, clients[1]),
            ('9012GHI', 'Ford', 'Focus', 2015, clients[2]),
            ('3456JKL', 'Audi', 'A3', 2022, clients[3]),
            ('7890MNP', 'Volkswagen', 'Golf', 2019, clients[0]),
        ]

        vehicles = []
        for plate, brand, model, year, client in vehicles_data:
            v, created = Vehicle.objects.get_or_create(
                workshop=workshop,
                plate=plate,
                defaults={
                    'brand': brand,
                    'model': model,
                    'year': year,
                    'client': client,
                }
            )
            vehicles.append(v)
            if created:
                self.stdout.write(f"Vehículo {plate} creado.")

        # 5. Crear Órdenes de Trabajo de ejemplo
        orders_data = [
            (vehicles[0], 'IN_PROGRESS', 'Cambio de aceite y filtros', 125000, 85.50),
            (vehicles[1], 'PENDING', 'Ruido extraño en motor al arrancar', 45000, 0.00),
            (vehicles[2], 'FINISHED', 'Cambio de pastillas de freno traseras', 180000, 120.00),
            (vehicles[3], 'DELIVERED', 'Revisión pre-ITV y luces', 12000, 60.00),
        ]

        for vehicle, status, desc, mileage, amount in orders_data:
            WorkOrder.objects.get_or_create(
                workshop=workshop,
                vehicle=vehicle,
                description=desc,
                defaults={
                    'status': status,
                    'mileage': mileage,
                    'total_amount': amount,
                }
            )
            self.stdout.write(f"Orden de trabajo para {vehicle.plate} creada.")

        # 6. Crear Presupuestos de ejemplo
        budgets_data = [
            (vehicles[1], 'Reparación de embrague completa', 450.00, False),
            (vehicles[4], 'Pintado de aleta delantera derecha', 200.00, True),
        ]

        for vehicle, desc, amount, is_appr in budgets_data:
            Budget.objects.get_or_create(
                workshop=workshop,
                vehicle=vehicle,
                description=desc,
                defaults={
                    'total_amount': amount,
                    'is_approved': is_appr,
                }
            )
            self.stdout.write(f"Presupuesto para {vehicle.plate} creado.")

        self.stdout.write(self.style.SUCCESS("¡Base de datos poblada con éxito!"))
