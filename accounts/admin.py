from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'department', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Department)