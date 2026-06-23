from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet
from . import views

router = DefaultRouter()
router.register(r'list', BookingViewSet, basename='booking')

urlpatterns = [

    path('', include(router.urls)),
    path('create/<int:item_id>/', views.create_booking_web, name='create_booking'),
    path('my/', views.my_bookings_web, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking_web, name='cancel_booking'),
]