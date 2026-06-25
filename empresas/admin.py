from django.contrib import admin
from django.utils.html import format_html
from .models import Empresa, Vehiculo, Conductor


class VehiculoInline(admin.TabularInline):
    model = Vehiculo
    extra = 0
    fields = ("placa", "tipo_vehiculo", "propiedad", "soat_vigencia", "rtm_vigencia", "activo")


class ConductorInline(admin.TabularInline):
    model = Conductor
    extra = 0
    fields = ("nombres_apellidos", "numero_documento", "licencia_vigencia", "examen_medico_vigencia", "es_reincidente", "activo")


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "nit", "nivel_pesv", "tipo_organizacion", "numero_vehiculos", "numero_conductores", "activa")
    list_filter = ("nivel_pesv", "tipo_organizacion", "misionalidad", "activa")
    search_fields = ("nombre", "nit", "representante_legal", "nombre_lider_pesv")
    inlines = [VehiculoInline, ConductorInline]
    fieldsets = (
        ("Identificación", {"fields": ("nombre", "nit", "tipo_organizacion", "misionalidad", "nivel_pesv", "sector_economico", "activa")}),
        ("Contacto", {"fields": ("direccion", "telefono", "email_contacto", "representante_legal")}),
        ("Líder PESV", {"fields": ("nombre_lider_pesv", "cargo_lider_pesv", "telefono_lider_pesv", "email_lider_pesv")}),
        ("Dimensionamiento", {"fields": ("numero_sedes", "numero_vehiculos", "numero_conductores", "numero_contratistas")}),
        ("Observaciones", {"fields": ("observaciones",)}),
    )


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("placa", "empresa", "tipo_vehiculo", "propiedad", "soat_vigencia", "alerta_soat", "rtm_vigencia", "alerta_rtm", "activo")
    list_filter = ("propiedad", "activo", "empresa")
    search_fields = ("placa", "empresa__nombre")

    def alerta_soat(self, obj):
        if obj.soat_vencido:
            return format_html('<span style="color:#c00;font-weight:bold;">VENCIDO</span>')
        return "Vigente"
    alerta_soat.short_description = "SOAT"

    def alerta_rtm(self, obj):
        if obj.rtm_vencida:
            return format_html('<span style="color:#c00;font-weight:bold;">VENCIDA</span>')
        return "Vigente"
    alerta_rtm.short_description = "RTM"


@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display = ("nombres_apellidos", "empresa", "numero_documento", "licencia_vigencia", "examen_medico_vigencia", "comparendos_verificado", "es_reincidente", "activo")
    list_filter = ("empresa", "es_reincidente", "comparendos_verificado", "activo")
    search_fields = ("nombres_apellidos", "numero_documento", "empresa__nombre")
    fieldsets = (
        ("Identificación", {"fields": ("empresa", "nombres_apellidos", "numero_documento", "tipo_vinculacion", "activo")}),
        ("1. Licencia de conducción", {"fields": ("licencia_categoria", "licencia_vigencia", "licencia_documento")}),
        ("2. Examen médico ocupacional", {"fields": ("examen_medico_fecha", "examen_medico_vigencia", "examen_medico_resultado", "examen_medico_documento")}),
        ("3. Comparendos e infracciones", {"fields": ("comparendos_verificado", "comparendos_fecha_verificacion", "comparendos_observaciones", "comparendos_soporte")}),
        ("4. Competencias para la movilidad segura", {"fields": ("competencias_fecha_evaluacion", "competencias_resultado", "competencias_documento")}),
        ("5. Jornada laboral y fatiga", {"fields": ("jornada_horas_promedio_dia", "fatiga_controles_aplicados", "fatiga_soporte")}),
        ("6. Reincidencia", {"fields": ("es_reincidente", "detalle_reincidencia", "plan_seguimiento_reincidencia")}),
    )
