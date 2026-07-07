from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'phone_number', 'is_verified', 'is_staff')
    list_filter = ('role', 'is_verified', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'business_name')
    ordering = ('email',)
    fieldsets = UserAdmin.fieldsets + (
        ('OYO profile', {'fields': ('role', 'phone_number', 'profile_picture', 'business_name', 'is_verified', 'email_otp')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('OYO profile', {'fields': ('email', 'role', 'phone_number', 'business_name')}),
    )

# Register your models here.
