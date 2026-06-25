from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib import messages
from .models import ProgramaAnualVerificacion, VisitaProgramada
from .forms import ProgramaAnualVerificacionForm, VisitaProgramadaForm


class ProgramaListView(LoginRequiredMixin, ListView):
    model = ProgramaAnualVerificacion
    template_name = "programa/lista.html"
    context_object_name = "programas"


class ProgramaDetailView(LoginRequiredMixin, DetailView):
    model = ProgramaAnualVerificacion
    template_name = "programa/detalle.html"
    context_object_name = "programa"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["visitas"] = self.object.visitas.select_related("empresa").all()
        return ctx


class ProgramaCreateView(LoginRequiredMixin, CreateView):
    model = ProgramaAnualVerificacion
    form_class = ProgramaAnualVerificacionForm
    template_name = "includes/form_generic.html"
    success_url = reverse_lazy("programa:lista")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Nuevo programa anual de verificación PESV"
        ctx["cancel_url"] = self.success_url
        return ctx

    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        messages.success(self.request, "Programa anual creado.")
        return super().form_valid(form)


class ProgramaUpdateView(LoginRequiredMixin, UpdateView):
    model = ProgramaAnualVerificacion
    form_class = ProgramaAnualVerificacionForm
    template_name = "includes/form_generic.html"

    def get_success_url(self):
        return reverse("programa:detalle", args=[self.object.pk])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = f"Editar programa {self.object}"
        ctx["cancel_url"] = self.get_success_url()
        return ctx


class VisitaCreateView(LoginRequiredMixin, CreateView):
    model = VisitaProgramada
    form_class = VisitaProgramadaForm
    template_name = "programa/visita_form.html"

    def get_initial(self):
        return {"programa": self.kwargs["programa_id"]}

    def get_success_url(self):
        return reverse("programa:detalle", args=[self.kwargs["programa_id"]])

    def form_valid(self, form):
        form.instance.programa_id = self.kwargs["programa_id"]
        messages.success(self.request, "Visita programada en el cronograma.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Programar visita de verificación"
        ctx["cancel_url"] = self.get_success_url()
        return ctx


class VisitaUpdateView(LoginRequiredMixin, UpdateView):
    model = VisitaProgramada
    form_class = VisitaProgramadaForm
    template_name = "programa/visita_form.html"

    def get_success_url(self):
        return reverse("programa:detalle", args=[self.object.programa_id])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = f"Editar visita - {self.object.empresa.nombre}"
        ctx["cancel_url"] = self.get_success_url()
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Visita actualizada.")
        return super().form_valid(form)
