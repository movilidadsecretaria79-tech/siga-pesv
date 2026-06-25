from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import PasoPESV, Componente, InstrumentoInspeccion


class CatalogoPESVView(LoginRequiredMixin, TemplateView):
    template_name = "pesv/catalogo.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        pasos = PasoPESV.objects.prefetch_related("componentes_principales").all()
        ctx["fases"] = [
            {
                "fase": fase_valor,
                "nombre": fase_nombre,
                "pasos": [p for p in pasos if p.fase == fase_valor],
            }
            for fase_valor, fase_nombre in PasoPESV.Fase.choices
        ]
        ctx["instrumentos"] = InstrumentoInspeccion.objects.filter(activo=True)
        return ctx
