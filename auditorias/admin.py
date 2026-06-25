from django.contrib import admin
from .models import Auditoria, ItemEvaluacion, Hallazgo, AccionMejora


class ItemEvaluacionInline(admin.TabularInline):
    model = ItemEvaluacion
    extra = 0


class AccionMejoraInline(admin.TabularInline):
    model = AccionMejora
    extra = 0


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ("empresa", "fecha_inicio", "fecha_fin", "estado", "total_no_conformidades")
    list_filter = ("estado", "empresa")
    filter_horizontal = ("equipo_auditor", "pasos_auditados", "componentes_auditados")
    inlines = [ItemEvaluacionInline]


@admin.register(Hallazgo)
class HallazgoAdmin(admin.ModelAdmin):
    list_display = ("auditoria", "tipo", "componente", "descripcion")
    list_filter = ("tipo", "auditoria__empresa")
    inlines = [AccionMejoraInline]


@admin.register(AccionMejora)
class AccionMejoraAdmin(admin.ModelAdmin):
    list_display = ("hallazgo", "responsable", "fecha_compromiso", "estado", "fecha_cierre")
    list_filter = ("estado",)
