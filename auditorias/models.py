from django.conf import settings
from django.db import models
from django.urls import reverse


class Auditoria(models.Model):
    """
    Ejecución de una auditoría/visita de verificación PESV a una empresa.
    Puede originarse desde una VisitaProgramada del programa anual, o
    crearse de forma independiente (auditoría extraordinaria).
    """

    class Estado(models.TextChoices):
        EN_PROCESO = "EN_PROCESO", "En proceso"
        FINALIZADA = "FINALIZADA", "Finalizada (pendiente de cierre)"
        CERRADA = "CERRADA", "Cerrada / informe emitido"

    visita = models.ForeignKey(
        "programa.VisitaProgramada", on_delete=models.SET_NULL, null=True, blank=True, related_name="auditorias"
    )
    empresa = models.ForeignKey("empresas.Empresa", on_delete=models.CASCADE, related_name="auditorias")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    lugar = models.CharField(max_length=255, blank=True)

    equipo_auditor = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="auditorias_realizadas", blank=True)
    pasos_auditados = models.ManyToManyField("pesv.PasoPESV", related_name="auditorias", blank=True)
    componentes_auditados = models.ManyToManyField("pesv.Componente", related_name="auditorias", blank=True)

    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.EN_PROCESO)
    resumen_ejecutivo = models.TextField(blank=True)
    elaborado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="informes_elaborados"
    )
    fecha_elaboracion_informe = models.DateField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Auditoría"
        verbose_name_plural = "Auditorías"
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return f"Auditoría {self.empresa.nombre} - {self.fecha_inicio}"

    def get_absolute_url(self):
        return reverse("auditorias:detalle", args=[self.pk])

    @property
    def duracion_horas(self):
        if self.hora_inicio and self.hora_fin:
            from datetime import datetime, date
            d1 = datetime.combine(date.today(), self.hora_inicio)
            d2 = datetime.combine(date.today(), self.hora_fin)
            delta = d2 - d1
            return round(delta.seconds / 3600, 1)
        return None

    @property
    def total_conformidades(self):
        return self.hallazgos.filter(tipo=Hallazgo.Tipo.CONFORMIDAD).count()

    @property
    def total_no_conformidades(self):
        return self.hallazgos.filter(tipo=Hallazgo.Tipo.NO_CONFORMIDAD).count()

    @property
    def total_observaciones(self):
        return self.hallazgos.filter(tipo=Hallazgo.Tipo.OBSERVACION).count()

    @property
    def total_recomendaciones(self):
        return self.hallazgos.filter(tipo=Hallazgo.Tipo.RECOMENDACION).count()


class ItemEvaluacion(models.Model):
    """Calificación de cada componente evaluado dentro de una auditoría (lista de verificación)."""

    class Calificacion(models.TextChoices):
        CUMPLE = "CUMPLE", "Cumple"
        CUMPLE_PARCIAL = "CUMPLE_PARCIAL", "Cumple parcialmente"
        NO_CUMPLE = "NO_CUMPLE", "No cumple"
        NO_APLICA = "NO_APLICA", "No aplica"
        SIN_EVALUAR = "SIN_EVALUAR", "Sin evaluar"

    auditoria = models.ForeignKey(Auditoria, on_delete=models.CASCADE, related_name="items_evaluados")
    componente = models.ForeignKey("pesv.Componente", on_delete=models.PROTECT, related_name="items_evaluados")
    calificacion = models.CharField(max_length=15, choices=Calificacion.choices, default=Calificacion.SIN_EVALUAR)
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = "Item evaluado"
        verbose_name_plural = "Items evaluados"
        unique_together = ("auditoria", "componente")
        ordering = ["componente__orden"]

    def __str__(self):
        return f"{self.componente.codigo} - {self.get_calificacion_display()}"


class Hallazgo(models.Model):
    """Conformidad, no conformidad, observación o recomendación detectada en la auditoría."""

    class Tipo(models.TextChoices):
        CONFORMIDAD = "CONFORMIDAD", "Conformidad"
        NO_CONFORMIDAD = "NO_CONFORMIDAD", "No conformidad"
        OBSERVACION = "OBSERVACION", "Observación"
        RECOMENDACION = "RECOMENDACION", "Recomendación"

    auditoria = models.ForeignKey(Auditoria, on_delete=models.CASCADE, related_name="hallazgos")
    componente = models.ForeignKey(
        "pesv.Componente", on_delete=models.SET_NULL, null=True, blank=True, related_name="hallazgos"
    )
    tipo = models.CharField(max_length=15, choices=Tipo.choices)
    descripcion = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Hallazgo"
        verbose_name_plural = "Hallazgos"
        ordering = ["tipo", "id"]

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.descripcion[:60]}"


class AccionMejora(models.Model):
    """Plan de mejoramiento: acción correctiva derivada de un hallazgo (típicamente una no conformidad)."""

    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        EN_PROCESO = "EN_PROCESO", "En proceso"
        CUMPLIDA = "CUMPLIDA", "Cumplida"
        VENCIDA = "VENCIDA", "Vencida"

    hallazgo = models.ForeignKey(Hallazgo, on_delete=models.CASCADE, related_name="acciones_mejora")
    accion = models.TextField("Acción de mejora")
    responsable = models.CharField(max_length=200, blank=True)
    fecha_compromiso = models.DateField("Fecha de cumplimiento comprometida")
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.PENDIENTE)
    fecha_cierre = models.DateField(null=True, blank=True)
    evidencia_cierre = models.FileField(upload_to="planes_mejora/evidencias_cierre/", blank=True, null=True)
    observaciones_seguimiento = models.TextField(blank=True)

    class Meta:
        verbose_name = "Acción del plan de mejoramiento"
        verbose_name_plural = "Plan de mejoramiento"
        ordering = ["fecha_compromiso"]

    def __str__(self):
        return f"Acción - {self.hallazgo.auditoria.empresa.nombre} ({self.fecha_compromiso})"

    @property
    def vencida(self):
        from django.utils import timezone
        return (
            self.estado not in (self.Estado.CUMPLIDA,)
            and self.fecha_compromiso < timezone.localdate()
        )

    def save(self, *args, **kwargs):
        if self.vencida and self.estado not in (self.Estado.CUMPLIDA,):
            self.estado = self.Estado.VENCIDA
        super().save(*args, **kwargs)
