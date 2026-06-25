from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "rol", "cargo", "empresa", "is_active")
    list_filter = ("rol", "is_active", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Información PESV", {"fields": ("rol", "cargo", "telefono", "firma", "empresa")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Información PESV", {"fields": ("rol", "cargo", "telefono", "empresa")}),
    )
