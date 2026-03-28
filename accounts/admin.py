from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Affiliate


@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'timezone', 'created_at']
    search_fields = ['name', 'country']
    ordering = ['name']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name', 'role', 'affiliate', 'is_active', 'date_joined']
    list_filter = ['role', 'affiliate', 'is_active', 'is_staff']
    search_fields = ['email', 'full_name', 'job_title']
    ordering = ['full_name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'job_title', 'phone', 'bio', 'profile_photo')}),
        ('Organisation', {'fields': ('role', 'affiliate')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'affiliate', 'password1', 'password2'),
        }),
    )
