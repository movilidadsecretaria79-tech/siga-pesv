from django.contrib import admin
from .models import DocumentoSoporte, EvidenciaEjecucion


@admin.register(DocumentoSoporte)
class DocumentoSoporteAdmin(admin.ModelAdmin):
    list_display = ("componente", "empresa", "version", "fecha_documento", "fecha_vigencia_hasta", "vigente", "cargado_por")
    list_filter = ("empresa", "vigente", "componente__paso_principal")
    search_fields = ("empresa__nombre", "componente__nombre")


@admin.register(EvidenciaEjecucion)
class EvidenciaEjecucionAdmin(admin.ModelAdmin):
    list_display = ("componente", "empresa", "tipo_archivo", "auditoria", "fecha_evidencia", "cargado_por")
    list_filter = ("empresa", "tipo_archivo", "componente__paso_principal")
    search_fields = ("empresa__nombre", "componente__nombre", "descripcion")
