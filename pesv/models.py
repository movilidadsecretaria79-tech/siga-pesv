from django.db import models


class PasoPESV(models.Model):
    """
    Catálogo oficial de los 24 pasos del PESV según la metodología de la
    Resolución 40595 de 2022 del Ministerio de Transporte, organizados en
    4 fases (PHVA).
    """

    class Fase(models.IntegerChoices):
        PLANIFICACION = 1, "Fase 1. Planificación del PESV"
        IMPLEMENTACION = 2, "Fase 2. Implementación y Ejecución del PESV"
        SEGUIMIENTO = 3, "Fase 3. Seguimiento por la Organización"
        MEJORA = 4, "Fase 4. Mejora Continua del PESV"

    class NivelAplicable(models.TextChoices):
        TODOS = "TODOS", "Aplica para todos los niveles"
        ESTANDAR_AVANZADO = "ESTANDAR_AVANZADO", "Aplica para nivel Estándar y Avanzado"
        AVANZADO = "AVANZADO", "Aplica solo para nivel Avanzado"

    numero = models.PositiveSmallIntegerField(unique=True)
    nombre = models.CharField(max_length=200)
    fase = models.IntegerField(choices=Fase.choices)
    nivel_aplicable = models.CharField(max_length=20, choices=NivelAplicable.choices, default=NivelAplicable.TODOS)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Paso del PESV"
        verbose_name_plural = "Catálogo: 24 pasos del PESV"
        ordering = ["numero"]

    def __str__(self):
        return f"Paso {self.numero}. {self.nombre}"

    def aplica_a_nivel(self, nivel_empresa):
        """nivel_empresa: 'BASICO' | 'ESTANDAR' | 'AVANZADO'"""
        if self.nivel_aplicable == self.NivelAplicable.TODOS:
            return True
        if self.nivel_aplicable == self.NivelAplicable.ESTANDAR_AVANZADO:
            return nivel_empresa in ("ESTANDAR", "AVANZADO")
        if self.nivel_aplicable == self.NivelAplicable.AVANZADO:
            return nivel_empresa == "AVANZADO"
        return True


class Componente(models.Model):
    """
    Componente/tema verificable dentro de un paso del PESV. Es el nivel de
    detalle real al que se sube documentación y evidencia de ejecución
    durante el programa de verificación y las auditorías (p. ej. dentro del
    Paso 16 "Inspección de vehículos y equipos" puede haber varios
    componentes verificables: estado de vehículos, SOAT, RTM, etc.).
    """

    class TipoEvidencia(models.TextChoices):
        DOCUMENTO = "DOCUMENTO", "Documento soporte únicamente"
        EJECUCION = "EJECUCION", "Evidencia de ejecución únicamente"
        AMBOS = "AMBOS", "Documento soporte y evidencia de ejecución"

    codigo = models.CharField(max_length=20, unique=True, help_text="Código corto, p. ej. C01")
    nombre = models.CharField(max_length=255)
    pregunta_verificacion = models.TextField(
        "Pregunta / criterio de verificación",
        blank=True,
        help_text="Pregunta orientadora que usará el auditor durante la visita.",
    )
    paso_principal = models.ForeignKey(
        PasoPESV, on_delete=models.PROTECT, related_name="componentes_principales"
    )
    pasos_relacionados = models.ManyToManyField(
        PasoPESV, blank=True, related_name="componentes_relacionados"
    )
    tipo_evidencia_esperada = models.CharField(
        max_length=10, choices=TipoEvidencia.choices, default=TipoEvidencia.AMBOS
    )
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Componente verificable"
        verbose_name_plural = "Catálogo: Componentes verificables"
        ordering = ["orden", "paso_principal__numero"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class InstrumentoInspeccion(models.Model):
    """Instrumentos de inspección y seguimiento usados por los auditores."""

    class Tipo(models.TextChoices):
        LISTA_CHEQUEO = "LISTA_CHEQUEO", "Lista de chequeo"
        ENTREVISTA = "ENTREVISTA", "Formato de entrevista"
        INSPECCION_FISICA = "INSPECCION_FISICA", "Formato de inspección física"
        ENCUESTA = "ENCUESTA", "Encuesta / cuestionario"
        OTRO = "OTRO", "Otro"

    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.LISTA_CHEQUEO)
    descripcion = models.TextField(blank=True)
    archivo_plantilla = models.FileField(upload_to="instrumentos/", blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Instrumento de inspección"
        verbose_name_plural = "Catálogo: Instrumentos de inspección y seguimiento"

    def __str__(self):
        return self.nombre
