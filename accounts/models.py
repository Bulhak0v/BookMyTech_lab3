from django.contrib.auth.models import AbstractUser
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва факультету/відділу")
    building = models.CharField(max_length=100, verbose_name="Корпус")

    def __str__(self):
        return f"{self.name} ({self.building})"

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Адміністратор'),
        ('user', 'Користувач'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"