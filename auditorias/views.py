from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string

from empresas.models import Empresa
from pesv.models import Componente, PasoPESV
from programa.models import VisitaProgramada
from .models import Auditoria, ItemEvaluacion, Hallazgo, AccionMejora
from .forms import AuditoriaForm, HallazgoForm, AccionMejoraForm, AccionMejoraSeguimientoForm, AuditoriaCierreForm


class AuditoriaListView(LoginRequiredMixin, ListView):
    model = Auditoria
    template_name = "auditorias/lista.html"
    context_object_name = "auditorias"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().select_related("empresa")
        estado = self.request.GET.get("estado")
        if estado:
            qs = qs.filter(estado=estado)
        return qs


class AuditoriaCrearView(LoginRequiredMixin, View):
    template_name = "auditorias/auditoria_form.html"

    def get(self, request):
        initial = {}
        visita = None
        empresa_id = request.GET.get("empresa")
        visita_id = request.GET.get("visita")
        if visita_id:
            visita = get_object_or_404(VisitaProgramada, pk=visita_id)
            initial = {
                "visita": visita.pk,
                "empresa": visita.empresa_id,
                "fecha_inicio": visita.fecha_programada,
                "pasos_auditados": list(visita.pasos_a_evaluar.values_list("pk", flat=True)),
                "equipo_auditor": list(visita.equipo_auditor.values_list("pk", flat=True)),
            }
        elif empresa_id:
            initial = {"empresa": empresa_id}
        form = AuditoriaForm(initial=initial)
        return render(request, self.template_name, {"form": form, "titulo": "Nueva auditoría / visita de verificación"})

    def post(self, request):
        form = AuditoriaForm(request.POST)
        if form.is_valid():
            auditoria = form.save()
            pasos = form.cleaned_data["pasos_auditados"]
            componentes = Componente.objects.filter(paso_principal__in=pasos, activo=True)
            auditoria.componentes_auditados.set(componentes)
            for c in componentes:
                ItemEvaluacion.objects.get_or_create(auditoria=auditoria, componente=c)
            messages.success(request, "Auditoría creada. Ya puede registrar la evaluación, hallazgos y plan de mejoramiento.")
            return redirect("auditorias:detalle", pk=auditoria.pk)
        return render(request, self.template_name, {"form": form, "titulo": "Nueva auditoría / visita de verificación"})


class AuditoriaDetailView(LoginRequiredMixin, DetailView):
    model = Auditoria
    template_name = "auditorias/detalle.html"
    context_object_name = "auditoria"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        items = self.object.items_evaluados.select_related("componente", "componente__paso_principal").order_by(
            "componente__paso_principal__numero", "componente__orden"
        )
        ctx["items"] = items
        ctx["calificaciones"] = ItemEvaluacion.Calificacion.choices
        ctx["hallazgos"] = self.object.hallazgos.select_related("componente").all()
        ctx["hallazgo_form"] = HallazgoForm(auditoria=self.object)
        ctx["accion_form"] = AccionMejoraForm()
        ctx["cierre_form"] = AuditoriaCierreForm(instance=self.object)
        ctx["tipos_hallazgo"] = Hallazgo.Tipo.choices
        return ctx


class ChecklistGuardarView(LoginRequiredMixin, View):
    def post(self, request, pk):
        auditoria = get_object_or_404(Auditoria, pk=pk)
        for item in auditoria.items_evaluados.all():
            cal_key = f"calificacion_{item.id}"
            obs_key = f"observaciones_{item.id}"
            if cal_key in request.POST:
                item.calificacion = request.POST.get(cal_key)
                item.observaciones = request.POST.get(obs_key, "")
                item.save()
        messages.success(request, "Lista de verificación actualizada.")
        return redirect("auditorias:detalle", pk=pk)


class HallazgoCrearView(LoginRequiredMixin, View):
    def post(self, request, pk):
        auditoria = get_object_or_404(Auditoria, pk=pk)
        form = HallazgoForm(request.POST, auditoria=auditoria)
        if form.is_valid():
            hallazgo = form.save(commit=False)
            hallazgo.auditoria = auditoria
            hallazgo.save()
            messages.success(request, f"{hallazgo.get_tipo_display()} registrada.")
        else:
            messages.error(request, "No se pudo registrar el hallazgo. Verifique los datos.")
        return redirect("auditorias:detalle", pk=pk)


class HallazgoEliminarView(LoginRequiredMixin, View):
    def post(self, request, pk, hallazgo_id):
        hallazgo = get_object_or_404(Hallazgo, pk=hallazgo_id, auditoria_id=pk)
        hallazgo.delete()
        messages.success(request, "Hallazgo eliminado.")
        return redirect("auditorias:detalle", pk=pk)


class AccionMejoraCrearView(LoginRequiredMixin, View):
    def post(self, request, pk, hallazgo_id):
        hallazgo = get_object_or_404(Hallazgo, pk=hallazgo_id, auditoria_id=pk)
        form = AccionMejoraForm(request.POST)
        if form.is_valid():
            accion = form.save(commit=False)
            accion.hallazgo = hallazgo
            accion.save()
            messages.success(request, "Acción de mejora agregada al plan de mejoramiento.")
        else:
            messages.error(request, "No se pudo agregar la acción de mejora.")
        return redirect("auditorias:detalle", pk=pk)


class AccionMejoraActualizarView(LoginRequiredMixin, View):
    def post(self, request, pk, accion_id):
        accion = get_object_or_404(AccionMejora, pk=accion_id, hallazgo__auditoria_id=pk)
        form = AccionMejoraSeguimientoForm(request.POST, request.FILES, instance=accion)
        if form.is_valid():
            form.save()
            messages.success(request, "Seguimiento del plan de mejoramiento actualizado.")
        else:
            messages.error(request, "No se pudo actualizar el seguimiento.")
        return redirect("auditorias:detalle", pk=pk)


class AuditoriaCerrarView(LoginRequiredMixin, View):
    def post(self, request, pk):
        auditoria = get_object_or_404(Auditoria, pk=pk)
        form = AuditoriaCierreForm(request.POST, instance=auditoria)
        if form.is_valid():
            auditoria = form.save(commit=False)
            auditoria.estado = Auditoria.Estado.CERRADA
            auditoria.elaborado_por = request.user
            auditoria.fecha_elaboracion_informe = timezone.localdate()
            if not auditoria.fecha_fin:
                auditoria.fecha_fin = timezone.localdate()
            auditoria.save()
            messages.success(request, "Auditoría cerrada. El informe ya puede generarse en PDF.")
        return redirect("auditorias:detalle", pk=pk)


class InformeAuditoriaView(LoginRequiredMixin, View):
    """Genera el informe de auditoría en HTML (vista previa) o PDF para descarga."""

    def get(self, request, pk):
        auditoria = get_object_or_404(Auditoria, pk=pk)
        contexto = self._contexto_informe(auditoria)
        if request.GET.get("formato") == "pdf":
            return self._render_pdf(contexto, auditoria)
        return render(request, "auditorias/informe.html", contexto)

    def _contexto_informe(self, auditoria):
        from documentos.models import DocumentoSoporte, EvidenciaEjecucion

        items = auditoria.items_evaluados.select_related("componente", "componente__paso_principal").order_by(
            "componente__paso_principal__numero"
        )
        componentes_ids = list(auditoria.componentes_auditados.values_list("pk", flat=True))
        documentos_revisados = DocumentoSoporte.objects.filter(
            empresa=auditoria.empresa, componente_id__in=componentes_ids, vigente=True
        ).select_related("componente")
        evidencias_revisadas = EvidenciaEjecucion.objects.filter(
            empresa=auditoria.empresa, componente_id__in=componentes_ids
        ).select_related("componente")

        return {
            "auditoria": auditoria,
            "items": items,
            "documentos_revisados": documentos_revisados,
            "evidencias_revisadas": evidencias_revisadas,
            "conformidades": auditoria.hallazgos.filter(tipo=Hallazgo.Tipo.CONFORMIDAD),
            "no_conformidades": auditoria.hallazgos.filter(tipo=Hallazgo.Tipo.NO_CONFORMIDAD),
            "observaciones": auditoria.hallazgos.filter(tipo=Hallazgo.Tipo.OBSERVACION),
            "recomendaciones": auditoria.hallazgos.filter(tipo=Hallazgo.Tipo.RECOMENDACION),
            "acciones_mejora": AccionMejora.objects.filter(hallazgo__auditoria=auditoria).select_related("hallazgo"),
            "equipo_auditor": auditoria.equipo_auditor.all(),
            "pasos_auditados": auditoria.pasos_auditados.all().order_by("numero"),
            "fecha_generacion": timezone.localdate(),
        }

    def _render_pdf(self, contexto, auditoria):
        from xhtml2pdf import pisa
        import io
        html = render_to_string("auditorias/informe_pdf.html", contexto)
        result = io.BytesIO()
        pisa.CreatePDF(io.StringIO(html), dest=result, encoding="utf-8")
        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        nombre = f"Informe_Auditoria_{auditoria.empresa.nit}_{auditoria.fecha_inicio}.pdf"
        response["Content-Disposition"] = f'attachment; filename="{nombre}"'
        return response
