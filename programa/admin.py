from django.contrib import admin
from .models import ProgramaAnualVerificacion, VisitaProgramada


class VisitaProgramadaInline(admin.TabularInline):
    model = VisitaProgramada
    extra = 0
    fields = ("empresa", "fecha_programada", "duracion_horas_estimada", "estado")
    show_change_link = True


@admin.register(ProgramaAnualVerificacion)
class ProgramaAnualVerificacionAdmin(admin.ModelAdmin):
    list_display = ("anio", "nombre", "estado", "fecha_aprobacion", "creado_por")
    list_filter = ("estado",)
    inlines = [VisitaProgramadaInline]


@admin.register(VisitaProgramada)
class VisitaProgramadaAdmin(admin.ModelAdmin):
    list_display = ("empresa", "programa", "fecha_programada", "estado", "duracion_horas_estimada")
    list_filter = ("programa", "estado", "empresa")
    filter_horizontal = ("pasos_a_evaluar", "componentes_a_evaluar", "equipo_auditor", "instrumentos")
