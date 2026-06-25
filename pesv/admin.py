from django.contrib import admin
from .models import PasoPESV, Componente, InstrumentoInspeccion


@admin.register(PasoPESV)
class PasoPESVAdmin(admin.ModelAdmin):
    list_display = ("numero", "nombre", "fase", "nivel_aplicable")
    list_filter = ("fase", "nivel_aplicable")
    ordering = ("numero",)


@admin.register(Componente)
class ComponenteAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "paso_principal", "tipo_evidencia_esperada", "activo")
    list_filter = ("paso_principal__fase", "tipo_evidencia_esperada", "activo")
    search_fields = ("codigo", "nombre")
    filter_horizontal = ("pasos_relacionados",)


@admin.register(InstrumentoInspeccion)
class InstrumentoInspeccionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "activo")
    list_filter = ("tipo", "activo")
