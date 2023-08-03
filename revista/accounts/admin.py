from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, PasswordResetCode

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name','is_active' , 'is_staff',
        'profile_image', 'birth_date', 'phone_number', 'gender'
        )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('profile_image', 'birth_date', 'phone_number', 'gender')
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('profile_image', 'birth_date', 'phone_number', 'gender')
        })
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PasswordResetCode)
