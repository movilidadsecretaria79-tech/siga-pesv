from django.conf import settings


def branding(request):
    return {
        "INSTITUCION_NOMBRE": getattr(settings, "INSTITUCION_NOMBRE", ""),
        "INSTITUCION_DEPENDENCIA": getattr(settings, "INSTITUCION_DEPENDENCIA", ""),
        "INSTITUCION_LOGO": getattr(settings, "INSTITUCION_LOGO", ""),
    }
