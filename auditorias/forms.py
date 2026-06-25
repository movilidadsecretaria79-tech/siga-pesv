from django import forms
from django.contrib.auth import get_user_model
from .models import Auditoria, Hallazgo, AccionMejora
from pesv.models import PasoPESV, Componente
from empresas.models import Empresa

Usuario = get_user_model()


class AuditoriaForm(forms.ModelForm):
    pasos_auditados = forms.ModelMultipleChoiceField(
        queryset=PasoPESV.objects.all().order_by("numero"),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Pasos del PESV auditados (de los 24)",
    )
    equipo_auditor = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.filter(is_active=True).order_by("first_name"),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Equipo auditor",
    )

    class Meta:
        model = Auditoria
        fields = [
            "visita", "empresa", "fecha_inicio", "fecha_fin", "hora_inicio", "hora_fin",
            "lugar", "equipo_auditor", "pasos_auditados",
        ]
        widgets = {
            "visita": forms.HiddenInput(),
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date"}),
            "hora_inicio": forms.TimeInput(attrs={"type": "time"}),
            "hora_fin": forms.TimeInput(attrs={"type": "time"}),
        }


class HallazgoForm(forms.ModelForm):
    class Meta:
        model = Hallazgo
        fields = ["tipo", "componente", "descripcion"]
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 2})}

    def __init__(self, *args, auditoria=None, **kwargs):
        super().__init__(*args, **kwargs)
        if auditoria is not None:
            self.fields["componente"].queryset = auditoria.componentes_auditados.all()
        self.fields["componente"].required = False


class AccionMejoraForm(forms.ModelForm):
    class Meta:
        model = AccionMejora
        fields = ["accion", "responsable", "fecha_compromiso"]
        widgets = {
            "accion": forms.Textarea(attrs={"rows": 2}),
            "fecha_compromiso": forms.DateInput(attrs={"type": "date"}),
        }


class AccionMejoraSeguimientoForm(forms.ModelForm):
    class Meta:
        model = AccionMejora
        fields = ["estado", "fecha_cierre", "evidencia_cierre", "observaciones_seguimiento"]
        widgets = {
            "fecha_cierre": forms.DateInput(attrs={"type": "date"}),
            "observaciones_seguimiento": forms.Textarea(attrs={"rows": 2}),
        }


class AuditoriaCierreForm(forms.ModelForm):
    class Meta:
        model = Auditoria
        fields = ["resumen_ejecutivo"]
        widgets = {"resumen_ejecutivo": forms.Textarea(attrs={"rows": 4})}
