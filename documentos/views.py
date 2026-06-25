from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.views import View

from empresas.models import Empresa
from pesv.models import Componente, PasoPESV
from .models import DocumentoSoporte, EvidenciaEjecucion
from .forms import DocumentoSoporteForm, EvidenciaEjecucionForm


class VerificacionRequisitosView(LoginRequiredMixin, View):
    """
    Apartado central de "Verificación de requisitos": por cada componente
    del catálogo PESV (agrupado por paso/fase) muestra si la empresa tiene
    documentación soporte vigente cargada y cuántas evidencias de ejecución
    existen, con accesos directos para cargar nuevos documentos o evidencias
    (documento y/o fotos).
    """

    template_name = "documentos/verificacion_requisitos.html"

    def get(self, request, empresa_id):
        empresa = get_object_or_404(Empresa, pk=empresa_id)
        componentes = (
            Componente.objects.filter(activo=True)
            .select_related("paso_principal")
            .order_by("paso_principal__numero", "orden")
        )
        filas = []
        for c in componentes:
            if not c.paso_principal.aplica_a_nivel(empresa.nivel_pesv):
                continue
            doc_vigente = (
                DocumentoSoporte.objects.filter(empresa=empresa, componente=c, vigente=True)
                .order_by("-fecha_carga")
                .first()
            )
            num_evidencias = EvidenciaEjecucion.objects.filter(empresa=empresa, componente=c).count()
            filas.append(
                {
                    "componente": c,
                    "doc_vigente": doc_vigente,
                    "num_evidencias": num_evidencias,
                }
            )
        # Agrupar por fase para la presentación
        fases = {}
        for fila in filas:
            fase = fila["componente"].paso_principal.get_fase_display()
            fases.setdefault(fase, []).append(fila)

        return render(
            request,
            self.template_name,
            {"empresa": empresa, "fases": fases},
        )


class DocumentoSoporteSubirView(LoginRequiredMixin, View):
    def get(self, request, empresa_id, componente_id):
        empresa = get_object_or_404(Empresa, pk=empresa_id)
        componente = get_object_or_404(Componente, pk=componente_id)
        form = DocumentoSoporteForm()
        return render(request, "documentos/subir_form.html", {
            "form": form, "empresa": empresa, "componente": componente,
            "titulo": f"Cargar documento soporte — {componente.nombre}",
        })

    def post(self, request, empresa_id, componente_id):
        empresa = get_object_or_404(Empresa, pk=empresa_id)
        componente = get_object_or_404(Componente, pk=componente_id)
        form = DocumentoSoporteForm(request.POST, request.FILES)
        if form.is_valid():
            # Marcar versiones anteriores como no vigentes
            DocumentoSoporte.objects.filter(empresa=empresa, componente=componente, vigente=True).update(vigente=False)
            doc = form.save(commit=False)
            doc.empresa = empresa
            doc.componente = componente
            doc.cargado_por = request.user
            doc.vigente = True
            doc.save()
            messages.success(request, "Documento cargado correctamente.")
            return redirect("documentos:verificacion_requisitos", empresa_id=empresa.pk)
        return render(request, "documentos/subir_form.html", {
            "form": form, "empresa": empresa, "componente": componente,
            "titulo": f"Cargar documento soporte — {componente.nombre}",
        })


class EvidenciaSubirView(LoginRequiredMixin, View):
    def get(self, request, empresa_id, componente_id):
        empresa = get_object_or_404(Empresa, pk=empresa_id)
        componente = get_object_or_404(Componente, pk=componente_id)
        form = EvidenciaEjecucionForm(empresa=empresa)
        return render(request, "documentos/subir_form.html", {
            "form": form, "empresa": empresa, "componente": componente,
            "titulo": f"Cargar evidencia de ejecución — {componente.nombre}",
        })

    def post(self, request, empresa_id, componente_id):
        empresa = get_object_or_404(Empresa, pk=empresa_id)
        componente = get_object_or_404(Componente, pk=componente_id)
        form = EvidenciaEjecucionForm(request.POST, request.FILES, empresa=empresa)
        if form.is_valid():
            ev = form.save(commit=False)
            ev.empresa = empresa
            ev.componente = componente
            ev.cargado_por = request.user
            ev.save()
            messages.success(request, "Evidencia cargada correctamente.")
            return redirect("documentos:verificacion_requisitos", empresa_id=empresa.pk)
        return render(request, "documentos/subir_form.html", {
            "form": form, "empresa": empresa, "componente": componente,
            "titulo": f"Cargar evidencia de ejecución — {componente.nombre}",
        })


class ComponenteEvidenciasView(LoginRequiredMixin, View):
    """Lista todos los documentos y evidencias cargados para un componente/empresa."""

    def get(self, request, empresa_id, componente_id):
        empresa = get_object_or_404(Empresa, pk=empresa_id)
        componente = get_object_or_404(Componente, pk=componente_id)
        documentos = DocumentoSoporte.objects.filter(empresa=empresa, componente=componente).order_by("-fecha_carga")
        evidencias = EvidenciaEjecucion.objects.filter(empresa=empresa, componente=componente).order_by("-fecha_carga")
        return render(request, "documentos/componente_evidencias.html", {
            "empresa": empresa, "componente": componente,
            "documentos": documentos, "evidencias": evidencias,
        })
