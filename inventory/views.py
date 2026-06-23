from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from .models import Equipment, Category, Location, MaintenanceLog
from .serializers import EquipmentSerializer, CategorySerializer, LocationSerializer, MaintenanceLogSerializer

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['name', 'serial_number']

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class MaintenanceLogViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceLog.objects.all()
    serializer_class = MaintenanceLogSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = MaintenanceLog.objects.all()
        equipment_id = self.request.query_params.get('equipment')
        if equipment_id:
            queryset = queryset.filter(equipment_id=equipment_id)
        return queryset


def equipment_list_web(request):
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')

    items = Equipment.objects.all()

    if search_query:
        items = items.filter(name__icontains=search_query)

    if category_id:
        items = items.filter(category_id=category_id)

    categories = Category.objects.all()

    return render(request, 'equipment_list.html', {
        'items': items,
        'categories': categories,
        'search_query': search_query
    })