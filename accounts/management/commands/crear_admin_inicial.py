"""
Crea (o sincroniza) un usuario administrador a partir de variables de entorno.

Pensado para plataformas como Render (plan gratuito) donde no siempre hay
acceso a una terminal interactiva para ejecutar `createsuperuser`. Cada vez
que se ejecuta (por ejemplo, en cada despliegue), deja la contraseña de ese
usuario igual a la definida en DJANGO_SUPERUSER_PASSWORD — así, si en algún
despliegue anterior quedó con un valor distinto, se corrige automáticamente
en el siguiente despliegue, sin necesitar terminal.

Variables de entorno usadas:
  DJANGO_SUPERUSER_USERNAME   (por defecto: "admin")
  DJANGO_SUPERUSER_EMAIL      (por defecto: "admin@example.com")
  DJANGO_SUPERUSER_PASSWORD   (obligatoria para crear/actualizar el usuario)
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class Command(BaseCommand):
    help = "Crea o sincroniza el usuario administrador a partir de variables de entorno."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        password = password.strip() if password else password

        if not password:
            self.stdout.write(self.style.WARNING(
                "DJANGO_SUPERUSER_PASSWORD no está definida: no se creó/actualizó ningún usuario."
            ))
            return

        usuario, creado = Usuario.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        usuario.email = email or usuario.email
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.is_active = True
        usuario.rol = "ADMIN"
        usuario.set_password(password)
        usuario.save()

        if creado:
            self.stdout.write(self.style.SUCCESS(f"Usuario administrador '{username}' creado."))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Usuario administrador '{username}' ya existía: contraseña sincronizada."
            ))
