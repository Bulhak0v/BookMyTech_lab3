from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import EquipmentViewSet, CategoryViewSet, LocationViewSet, MaintenanceLogViewSet

router = DefaultRouter()
router.register(r'items', EquipmentViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'maintenance', MaintenanceLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('web/', views.equipment_list_web, name='equipment_list'),
]