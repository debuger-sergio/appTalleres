from django.contrib import admin
from .models import Workshop, Client, Vehicle, WorkOrder, WorkOrderItem, Budget, BudgetItem

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'phone', 'created_at')
    search_fields = ('name', 'owner__username')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'workshop')
    list_filter = ('workshop',)
    search_fields = ('first_name', 'last_name', 'phone')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate', 'brand', 'model', 'client', 'workshop')
    list_filter = ('workshop', 'brand')
    search_fields = ('plate', 'brand', 'model')

class WorkOrderItemInline(admin.TabularInline):
    model = WorkOrderItem
    extra = 1

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'status', 'total_amount', 'workshop')
    list_filter = ('status', 'workshop')
    inlines = [WorkOrderItemInline]

class BudgetItemInline(admin.TabularInline):
    model = BudgetItem
    extra = 1

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'total_amount', 'is_approved', 'workshop')
    list_filter = ('workshop', 'is_approved')
    inlines = [BudgetItemInline]
