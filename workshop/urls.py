from django.urls import path
from . import views

# Definición de las rutas (URLs) de la aplicación de taller
urlpatterns = [
    # Dashboard principal
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Gestión de Clientes
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/new/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='client_edit'),
    
    # Gestión de Vehículos
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/new/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicles/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    path('vehicles/<int:pk>/edit/', views.VehicleUpdateView.as_view(), name='vehicle_edit'),
    
    # Gestión de Órdenes de Trabajo (OT)
    path('orders/', views.WorkOrderListView.as_view(), name='order_list'),
    path('orders/new/', views.WorkOrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/', views.WorkOrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/edit/', views.WorkOrderUpdateView.as_view(), name='order_edit'),
    
    # Gestión de Presupuestos
    path('budgets/', views.BudgetListView.as_view(), name='budget_list'),
    path('budgets/new/', views.BudgetCreateView.as_view(), name='budget_create'),
    path('budgets/<int:pk>/edit/', views.BudgetUpdateView.as_view(), name='budget_edit'),
    path('budgets/<int:pk>/approve/', views.approve_budget, name='budget_approve'),
    
    # Gestión de Facturación
    path('invoices/', views.InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('orders/<int:order_id>/generate-invoice/', views.generate_invoice, name='generate_invoice'),
    
    # Configuración inicial del taller
    path('setup/', views.WorkshopCreateView.as_view(), name='workshop_setup'),
]
