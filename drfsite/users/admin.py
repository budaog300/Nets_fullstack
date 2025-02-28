from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'last_login', 'is_superuser', 'email', 'photo', 'is_active',
                    'is_staff', 'date_joined', 'first_name', 'last_name', 'date_birth')
    list_display_links = ('id', 'username', 'email')
    list_editable = ('is_superuser', 'is_active', 'is_staff',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'date_birth', 'photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
