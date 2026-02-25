from django.test import TestCase, Client as TestClient
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Workshop, Client, Vehicle, WorkOrder, Budget, Invoice
import datetime

class WorkshopTestCase(TestCase):
    def setUp(self):
        # Crear usuarios para el test
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        
        # Crear talleres para cada usuario
        self.workshop1 = Workshop.objects.create(name="Taller 1", owner=self.user1)
        self.workshop2 = Workshop.objects.create(name="Taller 2", owner=self.user2)
        
        # Crear cliente y vehículo para taller 1
        self.client1 = Client.objects.create(workshop=self.workshop1, first_name="Juan", last_name="García", phone="123")
        self.vehicle1 = Vehicle.objects.create(workshop=self.workshop1, plate="1234abc", brand="Toyota", model="Corolla", client=self.client1)

    def test_plate_uppercase_conversion(self):
        """Verificar que la matrícula se guarde siempre en mayúsculas"""
        self.assertEqual(self.vehicle1.plate, "1234ABC")

    def test_multi_tenancy_filtering(self):
        """Verificar que un usuario no vea los clientes de otro taller"""
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('client_list'))
        self.assertEqual(len(response.context['clients']), 1)
        self.assertContains(response, "Juan García")
        
        self.client.login(username='user2', password='pass123')
        response = self.client.get(reverse('client_list'))
        self.assertEqual(len(response.context['clients']), 0)

    def test_vehicle_year_validation(self):
        """Probar que el año del vehículo tiene límites lógicos"""
        from django.core.exceptions import ValidationError
        
        # Año futuro no debería ser válido (esto se prueba mejor en el formulario o con full_clean)
        current_year = datetime.date.today().year
        v = Vehicle(workshop=self.workshop1, plate="TEST", brand="X", model="Y", year=current_year + 1, client=self.client1)
        with self.assertRaises(ValidationError):
            v.full_clean()

    def test_invoice_generation(self):
        """Probar que se puede generar una factura desde una OT"""
        order = WorkOrder.objects.create(
            workshop=self.workshop1,
            vehicle=self.vehicle1,
            description="Test Repair",
            mileage=1000,
            total_amount=150.00
        )
        
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('generate_invoice', args=[order.id]), follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Invoice.objects.filter(order=order).exists())
        invoice = Invoice.objects.get(order=order)
        self.assertEqual(invoice.total_amount, 150.00)

    def test_auth_protection(self):
        """Verificar que las vistas están protegidas"""
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302) # Redirección al login

    def test_dashboard_metrics(self):
        """Verificar que el dashboard muestra números correctos"""
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.context['total_clients'], 1)
        self.assertEqual(response.context['total_vehicles'], 1)

    def test_budget_approval_converts_to_order(self):
        """Verificar que aprobar un presupuesto crea una OT"""
        budget = Budget.objects.create(
            workshop=self.workshop1,
            vehicle=self.vehicle1,
            description="Presupuesto Test",
            total_amount=500.00
        )
        
        self.client.login(username='user1', password='pass123')
        self.client.get(reverse('budget_approve', args=[budget.id]))
        
        self.assertTrue(WorkOrder.objects.filter(description__contains=str(budget.id)).exists())
        budget.refresh_from_db()
        self.assertTrue(budget.is_approved)
