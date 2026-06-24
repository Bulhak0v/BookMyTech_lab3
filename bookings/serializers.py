from rest_framework import serializers
from .models import Booking
from django.utils import timezone


class BookingSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    equipment_name = serializers.ReadOnlyField(source='equipment.name')

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user', 'status', 'created_at']

    def validate(self, data):
        if data['start_date'] < timezone.now():
            raise serializers.ValidationError("Дата початку не може бути в минулому.")
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("Дата кінця має бути після дати початку.")

        overlapping_bookings = Booking.objects.filter(
            equipment=data['equipment'],
            start_date__lt=data['end_date'],
            end_date__gt=data['start_date']
        ).exclude(status='cancelled')

        if overlapping_bookings.exists():
            raise serializers.ValidationError("Ця техніка вже заброньована на обраний період.")

        return data