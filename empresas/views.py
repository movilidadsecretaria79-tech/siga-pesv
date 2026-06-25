from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Empresa, Vehiculo, Conductor
from .forms import EmpresaForm, VehiculoForm, ConductorForm


class EmpresaListView(LoginRequiredMixin, ListView):
    model = Empresa
    template_name = "empresas/lista.html"
    context_object_name = "empresas"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(nombre__icontains=q) | qs.filter(nit__icontains=q)
        return qs


class EmpresaDetailView(LoginRequiredMixin, DetailView):
    model = Empresa
    template_name = "empresas/detalle.html"
    context_object_name = "empresa"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["vehiculos"] = self.object.vehiculos.all()
        ctx["conductores"] = self.object.conductores.all()
        ctx["auditorias"] = self.object.auditorias.all().order_by("-fecha_inicio")[:10]
        return ctx


class EmpresaCreateView(LoginRequiredMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = "includes/form_generic.html"
    success_url = reverse_lazy("empresas:lista")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Registrar nueva empresa"
        ctx["cancel_url"] = self.success_url
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Empresa registrada correctamente.")
        return super().form_valid(form)


class EmpresaUpdateView(LoginRequiredMixin, UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = "includes/form_generic.html"

    def get_success_url(self):
        return reverse("empresas:detalle", args=[self.object.pk])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = f"Editar empresa: {self.object.nombre}"
        ctx["cancel_url"] = self.get_success_url()
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Empresa actualizada correctamente.")
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Vehículos
# ---------------------------------------------------------------------------
class VehiculoCreateView(LoginRequiredMixin, CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = "includes/form_generic.html"

    def get_initial(self):
        return {"empresa": self.kwargs["empresa_id"]}

    def get_success_url(self):
        return reverse("empresas:detalle", args=[self.kwargs["empresa_id"]])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Registrar vehículo"
        ctx["cancel_url"] = self.get_success_url()
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Vehículo registrado correctamente.")
        return super().form_valid(form)


class VehiculoUpdateView(LoginRequiredMixin, UpdateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = "includes/form_generic.html"

    def get_success_url(self):
        return reverse("empresas:detalle", args=[self.object.empresa_id])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = f"Editar vehículo: {self.object.placa}"
        ctx["cancel_url"] = self.get_success_url()
        return ctx


# ---------------------------------------------------------------------------
# Conductores
# ---------------------------------------------------------------------------
class ConductorCreateView(LoginRequiredMixin, CreateView):
    model = Conductor
    form_class = ConductorForm
    template_name = "includes/form_generic.html"

    def get_initial(self):
        return {"empresa": self.kwargs["empresa_id"]}

    def get_success_url(self):
        return reverse("empresas:detalle", args=[self.kwargs["empresa_id"]])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Registrar conductor"
        ctx["cancel_url"] = self.get_success_url()
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Conductor registrado correctamente.")
        return super().form_valid(form)


class ConductorUpdateView(LoginRequiredMixin, UpdateView):
    model = Conductor
    form_class = ConductorForm
    template_name = "includes/form_generic.html"

    def get_success_url(self):
        return reverse("empresas:detalle", args=[self.object.empresa_id])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = f"Gestión de conductor: {self.object.nombres_apellidos}"
        ctx["cancel_url"] = self.get_success_url()
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Información del conductor actualizada.")
        return super().form_valid(form)


class ConductorDetailView(LoginRequiredMixin, DetailView):
    model = Conductor
    template_name = "empresas/conductor_detalle.html"
    context_object_name = "conductor"
