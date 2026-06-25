"""
Crea (o actualiza) un usuario administrador a partir de variables de entorno.

Pensado para plataformas como Render (plan gratuito) donde no siempre hay
acceso a una terminal interactiva para ejecutar `createsuperuser`. Se puede
incluir de forma segura en el comando de "build" porque no hace nada si ya
existe un usuario con ese nombre y no se le pidió actualizar la contraseña.

Variables de entorno usadas:
  DJANGO_SUPERUSER_USERNAME   (por defecto: "admin")
  DJANGO_SUPERUSER_EMAIL      (por defecto: "admin@example.com")
  DJANGO_SUPERUSER_PASSWORD   (obligatoria para crear el usuario)
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class Command(BaseCommand):
    help = "Crea el usuario administrador inicial a partir de variables de entorno (idempotente)."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not password:
            self.stdout.write(self.style.WARNING(
                "DJANGO_SUPERUSER_PASSWORD no está definida: no se creó/actualizó ningún usuario."
            ))
            return

        usuario, creado = Usuario.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True, "rol": "ADMIN"},
        )
        if creado:
            usuario.set_password(password)
            usuario.is_staff = True
            usuario.is_superuser = True
            usuario.rol = "ADMIN"
            usuario.save()
            self.stdout.write(self.style.SUCCESS(f"Usuario administrador '{username}' creado."))
        else:
            self.stdout.write(f"El usuario '{username}' ya existía; no se modificó.")
