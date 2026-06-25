from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Usuario del sistema. Inicialmente solo se usan los roles ADMIN y AUDITOR
    (equipo interno de la Secretaría de Movilidad). El rol EMPRESA queda
    contemplado desde ya para una fase futura en la que las empresas
    auditadas puedan ingresar a cargar su propia documentación y evidencias.
    """

    class Rol(models.TextChoices):
        ADMIN = "ADMIN", "Administrador del sistema"
        AUDITOR = "AUDITOR", "Auditor / Verificador PESV"
        LIDER_EQUIPO = "LIDER_EQUIPO", "Líder de equipo auditor"
        EMPRESA = "EMPRESA", "Usuario de empresa auditada (futuro)"
        CONSULTA = "CONSULTA", "Solo consulta / directivo"

    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.AUDITOR)
    cargo = models.CharField("Cargo", max_length=150, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    firma = models.ImageField(
        "Firma digital (para informes)", upload_to="firmas/", blank=True, null=True
    )
    empresa = models.ForeignKey(
        "empresas.Empresa",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="usuarios",
        help_text="Solo aplica para usuarios con rol EMPRESA (fase futura).",
    )

    def __str__(self):
        nombre = self.get_full_name() or self.username
        return f"{nombre} ({self.get_rol_display()})"

    @property
    def es_auditor(self):
        return self.rol in (self.Rol.AUDITOR, self.Rol.LIDER_EQUIPO, self.Rol.ADMIN)
