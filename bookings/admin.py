from django.contrib import admin
from .models import Booking, Notification

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'user', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date')

admin.site.register(Notification)