"""
Configuración del proyecto SIGA-PESV
Sistema Integral de Gestión de Auditorías PESV
Secretaría de Movilidad de Villavicencio - Dirección de Planeación y Prospectiva

IMPORTANTE PARA DESPLIEGUE EN SERVIDOR:
- Local (por defecto): usa SQLite, no requiere configuración adicional.
- Servidor: defina la variable de entorno PESV_ENV=production y configure
  las variables DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, SECRET_KEY,
  ALLOWED_HOSTS. Ver README.md para instrucciones completas.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Seguridad / entorno
# ---------------------------------------------------------------------------
ENVIRONMENT = os.environ.get("PESV_ENV", "local")  # "local" o "production"

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-CAMBIAR-ESTA-CLAVE-ANTES-DE-PRODUCCION-pesv-villavicencio",
)

DEBUG = os.environ.get("DEBUG", "True" if ENVIRONMENT == "local" else "False") == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

CSRF_TRUSTED_ORIGINS = [
    o for o in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if o
]

# ---------------------------------------------------------------------------
# Aplicaciones
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "widget_tweaks",
    # Apps del sistema SIGA-PESV
    "accounts",
    "empresas",
    "pesv",
    "documentos",
    "programa",
    "auditorias",
    "seguimiento",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.branding",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ---------------------------------------------------------------------------
# Base de datos
# ---------------------------------------------------------------------------
if ENVIRONMENT == "production":
    if os.environ.get("DATABASE_URL"):
        # Forma simple recomendada para Render u otros proveedores que dan
        # una sola cadena de conexión (DATABASE_URL).
        import dj_database_url

        DATABASES = {
            "default": dj_database_url.config(
                env="DATABASE_URL", conn_max_age=600, ssl_require=True
            )
        }
    else:
        # Forma clásica con variables sueltas (servidor propio / VPS).
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": os.environ.get("DB_NAME", "pesv_db"),
                "USER": os.environ.get("DB_USER", "pesv_user"),
                "PASSWORD": os.environ.get("DB_PASSWORD", ""),
                "HOST": os.environ.get("DB_HOST", "localhost"),
                "PORT": os.environ.get("DB_PORT", "5432"),
            }
        }
    # Render (y la mayoría de plataformas en la nube) terminan el HTTPS en su
    # propio proxy y reenvían la petición por HTTP internamente; esta línea
    # le indica a Django que la conexión original sí era segura (HTTPS),
    # necesario para que el login y los formularios funcionen bien.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "accounts.Usuario"

# ---------------------------------------------------------------------------
# Internacionalización
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Archivos estáticos y multimedia (documentos/evidencias cargadas)
# ---------------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Tamaño máximo de archivo subido (25 MB) para documentos/fotos de evidencia
DATA_UPLOAD_MAX_MEMORY_SIZE = 25 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 25 * 1024 * 1024

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Autenticación / navegación
# ---------------------------------------------------------------------------
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"

# ---------------------------------------------------------------------------
# Datos institucionales (para reportes y plantillas)
# ---------------------------------------------------------------------------
INSTITUCION_NOMBRE = "Alcaldía de Villavicencio - Secretaría de Movilidad"
INSTITUCION_DEPENDENCIA = "Dirección de Planeación y Prospectiva"
INSTITUCION_LOGO = "img/logo_secretaria_movilidad.png"
