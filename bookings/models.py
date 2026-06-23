from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from inventory.models import Equipment

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Очікує підтвердження'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Скасовано'),
        ('completed', 'Завершено'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.equipment.name} ({self.start_date.date()})"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


@receiver([post_save, post_delete], sender=Booking)
def update_equipment_status(sender, instance, **kwargs):
    equipment = instance.equipment
    now = timezone.now()

    active_booking = Booking.objects.filter(
        equipment=equipment,
        status='confirmed',
        start_date__lte=now,
        end_date__gte=now
    ).exists()

    if equipment.status != 'repair':
        if active_booking:
            equipment.status = 'booked'
        else:
            equipment.status = 'available'

        equipment.save()