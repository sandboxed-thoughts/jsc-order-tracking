import imp
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, SimpleHistoryAdmin):
    model = CustomUser
    ordering = ['email']
    list_display = [
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
    ]
    fieldsets = (
        (None, {'fields': ('email', 'password',('first_name','last_name')),}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', ('password1', 'password2'), ('first_name','last_name'), ('is_active', 'is_staff', 'is_superuser'),'groups')}
        ),
    )