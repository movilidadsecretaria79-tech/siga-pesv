from django.conf import settings
from django.db import models


class ProgramaAnualVerificacion(models.Model):
    """Programa anual de verificación PESV de la Secretaría de Movilidad."""

    class Estado(models.TextChoices):
        BORRADOR = "BORRADOR", "Borrador"
        APROBADO = "APROBADO", "Aprobado"
        EN_EJECUCION = "EN_EJECUCION", "En ejecución"
        CERRADO = "CERRADO", "Cerrado"

    anio = models.PositiveIntegerField("Año", unique=True)
    nombre = models.CharField(max_length=255, blank=True)
    objetivo = models.TextField(blank=True)
    alcance = models.TextField(blank=True)
    estado = models.CharField(max_length=15, choices=Estado.choices, default=Estado.BORRADOR)
    fecha_aprobacion = models.DateField(null=True, blank=True)
    aprobado_por = models.CharField(max_length=200, blank=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Programa anual de verificación"
        verbose_name_plural = "Programas anuales de verificación"
        ordering = ["-anio"]

    def __str__(self):
        return self.nombre or f"Programa Anual de Verificación PESV {self.anio}"


class VisitaProgramada(models.Model):
    """Cronograma de visitas dentro del programa anual: empresa, fecha, equipo, criterios e instrumentos."""

    class Estado(models.TextChoices):
        PROGRAMADA = "PROGRAMADA", "Programada"
        REPROGRAMADA = "REPROGRAMADA", "Reprogramada"
        REALIZADA = "REALIZADA", "Realizada"
        CANCELADA = "CANCELADA", "Cancelada"

    programa = models.ForeignKey(ProgramaAnualVerificacion, on_delete=models.CASCADE, related_name="visitas")
    empresa = models.ForeignKey("empresas.Empresa", on_delete=models.CASCADE, related_name="visitas_programadas")
    fecha_programada = models.DateField()
    fecha_real = models.DateField(null=True, blank=True)
    duracion_horas_estimada = models.DecimalField(max_digits=4, decimal_places=1, default=4)

    pasos_a_evaluar = models.ManyToManyField(
        "pesv.PasoPESV", related_name="visitas_programadas", blank=True,
        help_text="Número de pasos del PESV (de los 24) a evaluar en esta visita.",
    )
    componentes_a_evaluar = models.ManyToManyField(
        "pesv.Componente", related_name="visitas_programadas", blank=True,
    )
    equipo_auditor = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="visitas_asignadas", blank=True,
        limit_choices_to={"is_active": True},
    )
    instrumentos = models.ManyToManyField(
        "pesv.InstrumentoInspeccion", related_name="visitas_programadas", blank=True
    )
    estado = models.CharField(max_length=15, choices=Estado.choices, default=Estado.PROGRAMADA)
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = "Visita programada"
        verbose_name_plural = "Cronograma de visitas"
        ordering = ["fecha_programada"]

    def __str__(self):
        return f"Visita a {self.empresa.nombre} - {self.fecha_programada}"
