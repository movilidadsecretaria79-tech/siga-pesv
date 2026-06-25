from django.conf import settings
from django.db import models


class DocumentoSoporte(models.Model):
    """
    Documentación soporte vigente que la empresa mantiene para cada
    componente del PESV (PESV vigente, política, designación del líder,
    actas del comité, diagnóstico, matrices, procedimientos, etc.).
    Es documentación "de estado" de la empresa, independiente de una
    auditoría puntual, y se reutiliza en auditorías sucesivas.
    """

    empresa = models.ForeignKey("empresas.Empresa", on_delete=models.CASCADE, related_name="documentos_soporte")
    componente = models.ForeignKey("pesv.Componente", on_delete=models.PROTECT, related_name="documentos_soporte")
    archivo = models.FileField(upload_to="documentos_soporte/%Y/")
    descripcion = models.CharField(max_length=255, blank=True)
    fecha_documento = models.DateField("Fecha del documento", null=True, blank=True)
    fecha_vigencia_hasta = models.DateField("Vigente hasta", null=True, blank=True)
    version = models.PositiveIntegerField(default=1)
    vigente = models.BooleanField(
        default=True, help_text="Desmarcar cuando este documento sea reemplazado por una versión más reciente."
    )
    cargado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Documento soporte"
        verbose_name_plural = "Documentos soporte"
        ordering = ["-fecha_carga"]

    def __str__(self):
        return f"{self.componente.nombre} - {self.empresa.nombre} (v{self.version})"

    @property
    def vencido(self):
        from django.utils import timezone
        return bool(self.fecha_vigencia_hasta) and self.fecha_vigencia_hasta < timezone.localdate()


class EvidenciaEjecucion(models.Model):
    """
    Evidencia de la ejecución/implementación real de un componente del
    PESV: puede ser documental (registros, listados, actas, formatos
    diligenciados) o fotográfica (estado de vehículos, botiquines,
    señalización, capacitaciones en sitio, etc.).
    """

    class TipoArchivo(models.TextChoices):
        DOCUMENTO = "DOCUMENTO", "Documento"
        FOTO = "FOTO", "Fotografía"

    empresa = models.ForeignKey("empresas.Empresa", on_delete=models.CASCADE, related_name="evidencias_ejecucion")
    componente = models.ForeignKey("pesv.Componente", on_delete=models.PROTECT, related_name="evidencias_ejecucion")
    auditoria = models.ForeignKey(
        "auditorias.Auditoria", on_delete=models.SET_NULL, null=True, blank=True, related_name="evidencias"
    )
    tipo_archivo = models.CharField(max_length=10, choices=TipoArchivo.choices, default=TipoArchivo.DOCUMENTO)
    archivo = models.FileField(upload_to="evidencias_ejecucion/%Y/")
    descripcion = models.CharField(max_length=255, blank=True)
    fecha_evidencia = models.DateField("Fecha de la evidencia", null=True, blank=True)
    cargado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Evidencia de ejecución"
        verbose_name_plural = "Evidencias de ejecución"
        ordering = ["-fecha_carga"]

    def __str__(self):
        return f"Evidencia {self.componente.nombre} - {self.empresa.nombre}"

    @property
    def es_foto(self):
        return self.tipo_archivo == self.TipoArchivo.FOTO
