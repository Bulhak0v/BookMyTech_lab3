from django.contrib import admin
from .models import Equipment, Category, Location, MaintenanceLog

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'category', 'status', 'location')
    list_filter = ('status', 'category')
    search_fields = ('name', 'serial_number')

admin.site.register(Category)
admin.site.register(Location)
admin.site.register(MaintenanceLog)