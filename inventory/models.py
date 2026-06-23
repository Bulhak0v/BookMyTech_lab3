from django.db import models
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    requires_approval = models.BooleanField(default=False)  # Чи потрібен дозвіл адміна

    def __str__(self):
        return self.name


class Location(models.Model):
    room_number = models.CharField(max_length=20)
    shelf = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Room {self.room_number}, Shelf {self.shelf}"


class Equipment(models.Model):
    STATUS_CHOICES = (
        ('available', 'Доступно'),
        ('booked', 'Заброньовано'),
        ('repair', 'В ремонті'),
    )

    name = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='equipments')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to='equipment_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    def is_currently_free(self):
        if self.status == 'repair':
            return False
        return not self.bookings.filter(
            status='confirmed',
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).exists()

    @property
    def current_status(self):
        if self.status == 'repair':
            return 'repair'

        now = timezone.now()
        is_taken = self.bookings.filter(
            status='confirmed',
            start_date__lte=now,
            end_date__gte=now
        ).exists()

        return 'booked' if is_taken else 'available'


class MaintenanceLog(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='maintenance_logs')
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                              limit_choices_to={'role': 'admin'})

    issue_description = models.TextField(verbose_name="Опис проблеми")
    repair_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Вартість ремонту")

    date_reported = models.DateTimeField(auto_now_add=True, verbose_name="Дата звіту")
    date_fixed = models.DateTimeField(null=True, blank=True, verbose_name="Дата виправлення")

    def __str__(self):
        return f"Ремонт {self.equipment.name} від {self.date_reported.date()}"