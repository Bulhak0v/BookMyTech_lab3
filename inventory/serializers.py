from rest_framework import serializers
from .models import Equipment, Category, Location, MaintenanceLog

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class EquipmentSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='current_status')
    category_name = serializers.ReadOnlyField(source='category.name')
    location_name = serializers.StringRelatedField(source='location')

    class Meta:
        model = Equipment
        fields = ['id', 'name', 'serial_number', 'category', 'category_name',
                  'location', 'location_name', 'status', 'description', 'image']

class MaintenanceLogSerializer(serializers.ModelSerializer):
    equipment_name = serializers.ReadOnlyField(source='equipment.name')
    admin_name = serializers.ReadOnlyField(source='admin.username')

    class Meta:
        model = MaintenanceLog
        fields = '__all__'