from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Workshop, Client, Vehicle, WorkOrder, Budget, Invoice

# Mixin base para asegurar que el usuario tenga un taller configurado y filtrar datos por taller
class WorkshopBaseMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        # Redirigir a configuración si el usuario no tiene taller asociado
        if not Workshop.objects.filter(owner=request.user).exists() and self.__class__.__name__ != 'WorkshopCreateView':
            return redirect('workshop_setup')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Filtrar los resultados para mostrar solo los que pertenecen al taller del usuario actual
        workshop = Workshop.objects.filter(owner=self.request.user).first()
        return self.model.objects.filter(workshop=workshop)

    def form_valid(self, form):
        # Asignar automáticamente el taller del usuario al guardar un formulario
        workshop = Workshop.objects.filter(owner=self.request.user).first()
        form.instance.workshop = workshop
        return super().form_valid(form)

# Vista del panel principal con métricas clave
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'workshop/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not Workshop.objects.filter(owner=request.user).exists():
            return redirect('workshop_setup')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workshop = Workshop.objects.filter(owner=self.request.user).first()
        if workshop:
            context['workshop'] = workshop
            context['total_clients'] = Client.objects.filter(workshop=workshop).count()
            context['total_vehicles'] = Vehicle.objects.filter(workshop=workshop).count()
            context['pending_orders'] = WorkOrder.objects.filter(workshop=workshop, status='PENDING').count()
            context['in_progress_orders'] = WorkOrder.objects.filter(workshop=workshop, status='IN_PROGRESS').count()
            context['recent_orders'] = WorkOrder.objects.filter(workshop=workshop).order_by('-created_at')[:5]
        return context

# Vistas para Clientes
class ClientListView(WorkshopBaseMixin, ListView):
    model = Client
    template_name = 'workshop/client_list.html'
    context_object_name = 'clients'

class ClientCreateView(WorkshopBaseMixin, CreateView):
    model = Client
    fields = ['first_name', 'last_name', 'phone', 'email', 'dni', 'address']
    template_name = 'workshop/form.html'
    success_url = reverse_lazy('client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Cliente'
        return context

class ClientUpdateView(WorkshopBaseMixin, UpdateView):
    model = Client
    fields = ['first_name', 'last_name', 'phone', 'email', 'dni', 'address']
    template_name = 'workshop/form.html'
    success_url = reverse_lazy('client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar Cliente: {self.object}'
        return context

class ClientDetailView(WorkshopBaseMixin, DetailView):
    model = Client
    template_name = 'workshop/client_detail.html'
    context_object_name = 'client'

# Vistas para Vehículos
class VehicleListView(WorkshopBaseMixin, ListView):
    model = Vehicle
    template_name = 'workshop/vehicle_list.html'
    context_object_name = 'vehicles'

class VehicleCreateView(WorkshopBaseMixin, CreateView):
    model = Vehicle
    fields = ['plate', 'brand', 'model', 'year', 'vin', 'client']
    template_name = 'workshop/form.html'
    success_url = reverse_lazy('vehicle_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Vehículo'
        return context

class VehicleUpdateView(WorkshopBaseMixin, UpdateView):
    model = Vehicle
    fields = ['plate', 'brand', 'model', 'year', 'vin', 'client']
    template_name = 'workshop/form.html'
    success_url = reverse_lazy('vehicle_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar Vehículo: {self.object.plate}'
        return context

class VehicleDetailView(WorkshopBaseMixin, DetailView):
    model = Vehicle
    template_name = 'workshop/vehicle_detail.html'
    context_object_name = 'vehicle'

# Vista para la configuración inicial del taller por parte del usuario
class WorkshopCreateView(LoginRequiredMixin, CreateView):
    model = Workshop
    fields = ['name', 'logo', 'tax_id', 'address', 'phone', 'email']
    template_name = 'workshop/form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Configura tu Taller'
        return context

# Vistas para Órdenes de Trabajo (OT)
class WorkOrderListView(WorkshopBaseMixin, ListView):
    model = WorkOrder
    template_name = 'workshop/order_list.html'
    context_object_name = 'orders'

class WorkOrderCreateView(WorkshopBaseMixin, CreateView):
    model = WorkOrder
    fields = ['vehicle', 'status', 'description', 'mileage', 'total_amount']
    template_name = 'workshop/form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Orden de Trabajo'
        return context

class WorkOrderUpdateView(WorkshopBaseMixin, UpdateView):
    model = WorkOrder
    fields = ['status', 'description', 'mileage', 'total_amount']
    template_name = 'workshop/form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar Orden #{self.object.id}'
        return context

class WorkOrderDetailView(WorkshopBaseMixin, DetailView):
    model = WorkOrder
    template_name = 'workshop/order_detail.html'
    context_object_name = 'order'

# Vistas para Presupuestos
class BudgetListView(WorkshopBaseMixin, ListView):
    model = Budget
    template_name = 'workshop/budget_list.html'
    context_object_name = 'budgets'

class BudgetCreateView(WorkshopBaseMixin, CreateView):
    model = Budget
    fields = ['vehicle', 'description', 'total_amount']
    template_name = 'workshop/form.html'
    success_url = reverse_lazy('budget_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Presupuesto'
        return context

class BudgetUpdateView(WorkshopBaseMixin, UpdateView):
    model = Budget
    fields = ['description', 'total_amount', 'is_approved']
    template_name = 'workshop/form.html'
    success_url = reverse_lazy('budget_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar Presupuesto #{self.object.id}'
        return context

# Función para aprobar un presupuesto y convertirlo automáticamente en una Orden de Trabajo
def approve_budget(request, pk):
    budget = Budget.objects.get(pk=pk, workshop__owner=request.user)
    budget.is_approved = True
    budget.save()
    
    # Crear la Orden de Trabajo basada en los datos del presupuesto
    WorkOrder.objects.create(
        workshop=budget.workshop,
        vehicle=budget.vehicle,
        description=f"Basado en presupuesto #{budget.id}: {budget.description}",
        mileage=0, 
        total_amount=budget.total_amount,
        status='PENDING'
    )
    messages.success(request, f"Presupuesto #{budget.id} aprobado y convertido en Orden de Trabajo.")
    return redirect('order_list')

# Vistas para Facturas
class InvoiceListView(WorkshopBaseMixin, ListView):
    model = Invoice
    template_name = 'workshop/invoice_list.html'
    context_object_name = 'invoices'

class InvoiceDetailView(WorkshopBaseMixin, DetailView):
    model = Invoice
    template_name = 'workshop/invoice_detail.html'
    context_object_name = 'invoice'

# Función para generar una factura a partir de una orden de trabajo finalizada
def generate_invoice(request, order_id):
    order = WorkOrder.objects.get(pk=order_id, workshop__owner=request.user)
    
    # Evitar duplicados
    if hasattr(order, 'invoice'):
        messages.warning(request, "Esta orden ya tiene una factura generada.")
        return redirect('invoice_detail', pk=order.invoice.id)
    
    # Generación de número de factura simple
    import datetime
    invoice_number = f"FAC-{order.id}-{datetime.date.today().year}"
    
    invoice = Invoice.objects.create(
        workshop=order.workshop,
        order=order,
        invoice_number=invoice_number,
        total_amount=order.total_amount
    )
    
    messages.success(request, f"Factura {invoice_number} generada con éxito.")
    return redirect('invoice_detail', pk=invoice.id)
