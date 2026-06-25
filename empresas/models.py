from django.db import models
from django.urls import reverse


class Empresa(models.Model):
    """Empresa u organización sujeta a verificación del PESV."""

    class TipoOrganizacion(models.TextChoices):
        PUBLICA = "PUBLICA", "Pública"
        PRIVADA = "PRIVADA", "Privada"
        MIXTA = "MIXTA", "Mixta"

    class Misionalidad(models.TextChoices):
        TRANSPORTE = "TRANSPORTE", "Misionalidad 1: Prestación del servicio de transporte"
        OTRA = "OTRA", "Misionalidad 2: Otra (contrata o administra conductores)"

    class Nivel(models.TextChoices):
        BASICO = "BASICO", "Básico"
        ESTANDAR = "ESTANDAR", "Estándar"
        AVANZADO = "AVANZADO", "Avanzado"

    nombre = models.CharField("Razón social", max_length=255)
    nit = models.CharField("NIT", max_length=30, unique=True)
    tipo_organizacion = models.CharField(
        max_length=10, choices=TipoOrganizacion.choices, default=TipoOrganizacion.PRIVADA
    )
    misionalidad = models.CharField(
        max_length=12, choices=Misionalidad.choices, default=Misionalidad.OTRA
    )
    nivel_pesv = models.CharField(
        "Nivel PESV", max_length=10, choices=Nivel.choices, default=Nivel.BASICO,
        help_text="Determina qué pasos del PESV son exigibles a la organización.",
    )
    sector_economico = models.CharField(max_length=150, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    email_contacto = models.EmailField(blank=True)
    representante_legal = models.CharField(max_length=200, blank=True)

    nombre_lider_pesv = models.CharField("Líder del PESV designado", max_length=200, blank=True)
    cargo_lider_pesv = models.CharField(max_length=150, blank=True)
    telefono_lider_pesv = models.CharField(max_length=30, blank=True)
    email_lider_pesv = models.EmailField(blank=True)

    numero_sedes = models.PositiveIntegerField("Cantidad de sedes", default=1)
    numero_vehiculos = models.PositiveIntegerField("Cantidad de vehículos", default=0)
    numero_conductores = models.PositiveIntegerField("Cantidad de conductores/colaboradores", default=0)
    numero_contratistas = models.PositiveIntegerField("Cantidad de contratistas", default=0)

    activa = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} (NIT {self.nit})"

    def get_absolute_url(self):
        return reverse("empresas:detalle", args=[self.pk])


class Vehiculo(models.Model):
    class Propiedad(models.TextChoices):
        PROPIO = "PROPIO", "Propio"
        CONTRATADO = "CONTRATADO", "Contratado / tercerizado"
        LEASING = "LEASING", "Leasing / Renting"

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="vehiculos")
    placa = models.CharField(max_length=20)
    tipo_vehiculo = models.CharField(max_length=100, blank=True)
    modelo = models.CharField("Modelo / año", max_length=20, blank=True)
    propiedad = models.CharField(max_length=12, choices=Propiedad.choices, default=Propiedad.PROPIO)
    soat_vigencia = models.DateField("Vigencia SOAT", null=True, blank=True)
    rtm_vigencia = models.DateField("Vigencia revisión técnico-mecánica", null=True, blank=True)
    estado_llantas_sistemas_seguridad = models.CharField(
        "Estado llantas / sistemas de seguridad", max_length=200, blank=True
    )
    activo = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ["empresa", "placa"]

    def __str__(self):
        return f"{self.placa} - {self.empresa.nombre}"

    @property
    def soat_vencido(self):
        from django.utils import timezone
        return bool(self.soat_vigencia) and self.soat_vigencia < timezone.localdate()

    @property
    def rtm_vencida(self):
        from django.utils import timezone
        return bool(self.rtm_vigencia) and self.rtm_vigencia < timezone.localdate()


class Conductor(models.Model):
    """
    Gestión de conductores: agrupa los puntos de verificación específicos
    solicitados: licencias, exámenes médicos, comparendos, competencias,
    fatiga y reincidencia.
    """

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="conductores")
    nombres_apellidos = models.CharField(max_length=200)
    numero_documento = models.CharField(max_length=30)
    tipo_vinculacion = models.CharField(
        max_length=50, blank=True, help_text="Empleado directo, contratista, tercerizado, etc."
    )

    # 1. Licencia de conducción vigente
    licencia_categoria = models.CharField(max_length=20, blank=True)
    licencia_vigencia = models.DateField("Vigencia licencia de conducción", null=True, blank=True)
    licencia_documento = models.FileField(upload_to="conductores/licencias/", blank=True, null=True)

    # 2. Examen médico ocupacional
    examen_medico_fecha = models.DateField("Fecha último examen médico", null=True, blank=True)
    examen_medico_vigencia = models.DateField("Vigencia examen médico", null=True, blank=True)
    examen_medico_resultado = models.CharField(
        max_length=20,
        choices=[("APTO", "Apto"), ("APTO_RESTRICCIONES", "Apto con restricciones"), ("NO_APTO", "No apto")],
        blank=True,
    )
    examen_medico_documento = models.FileField(upload_to="conductores/examenes_medicos/", blank=True, null=True)

    # 3. Verificación de comparendos e infracciones
    comparendos_verificado = models.BooleanField("Comparendos verificados", default=False)
    comparendos_fecha_verificacion = models.DateField(null=True, blank=True)
    comparendos_observaciones = models.TextField(blank=True)
    comparendos_soporte = models.FileField(upload_to="conductores/comparendos/", blank=True, null=True)

    # 4. Evaluación de competencias para la movilidad segura
    competencias_fecha_evaluacion = models.DateField(null=True, blank=True)
    competencias_resultado = models.CharField(max_length=100, blank=True)
    competencias_documento = models.FileField(upload_to="conductores/competencias/", blank=True, null=True)

    # 5. Control de jornadas laborales y fatiga
    jornada_horas_promedio_dia = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    fatiga_controles_aplicados = models.TextField(
        "Controles de fatiga aplicados", blank=True,
        help_text="Pausas activas, rotación de turnos, monitoreo de horas de conducción, etc.",
    )
    fatiga_soporte = models.FileField(upload_to="conductores/fatiga/", blank=True, null=True)

    # 6. Seguimiento a conductores reincidentes
    es_reincidente = models.BooleanField("Conductor reincidente", default=False)
    detalle_reincidencia = models.TextField(blank=True)
    plan_seguimiento_reincidencia = models.TextField(blank=True)

    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Conductor"
        verbose_name_plural = "Conductores"
        ordering = ["empresa", "nombres_apellidos"]
        unique_together = ("empresa", "numero_documento")

    def __str__(self):
        return f"{self.nombres_apellidos} - {self.empresa.nombre}"

    @property
    def licencia_vencida(self):
        from django.utils import timezone
        return bool(self.licencia_vigencia) and self.licencia_vigencia < timezone.localdate()

    @property
    def examen_medico_vencido(self):
        from django.utils import timezone
        return bool(self.examen_medico_vigencia) and self.examen_medico_vigencia < timezone.localdate()

    @property
    def alertas(self):
        """Lista de alertas activas de cumplimiento para este conductor."""
        alertas = []
        if self.licencia_vencida:
            alertas.append("Licencia de conducción vencida")
        if self.examen_medico_vencido:
            alertas.append("Examen médico ocupacional vencido")
        if not self.comparendos_verificado:
            alertas.append("Comparendos no verificados")
        if self.es_reincidente and not self.plan_seguimiento_reincidencia:
            alertas.append("Reincidente sin plan de seguimiento")
        return alertas
