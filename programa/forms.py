from django import forms
from django.contrib.auth import get_user_model
from .models import ProgramaAnualVerificacion, VisitaProgramada
from pesv.models import PasoPESV, Componente, InstrumentoInspeccion

Usuario = get_user_model()


class ProgramaAnualVerificacionForm(forms.ModelForm):
    class Meta:
        model = ProgramaAnualVerificacion
        exclude = ["creado_por", "creado_en"]
        widgets = {
            "objetivo": forms.Textarea(attrs={"rows": 3}),
            "alcance": forms.Textarea(attrs={"rows": 3}),
            "fecha_aprobacion": forms.DateInput(attrs={"type": "date"}),
        }


class VisitaProgramadaForm(forms.ModelForm):
    pasos_a_evaluar = forms.ModelMultipleChoiceField(
        queryset=PasoPESV.objects.all().order_by("numero"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Criterios de evaluación: pasos del PESV a evaluar (de los 24)",
    )
    equipo_auditor = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.filter(is_active=True).order_by("first_name"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Equipo auditor / verificador",
    )
    instrumentos = forms.ModelMultipleChoiceField(
        queryset=InstrumentoInspeccion.objects.filter(activo=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Instrumentos de inspección y seguimiento",
    )

    class Meta:
        model = VisitaProgramada
        fields = [
            "empresa", "fecha_programada", "fecha_real", "duracion_horas_estimada",
            "pasos_a_evaluar", "componentes_a_evaluar", "equipo_auditor", "instrumentos",
            "estado", "observaciones",
        ]
        widgets = {
            "fecha_programada": forms.DateInput(attrs={"type": "date"}),
            "fecha_real": forms.DateInput(attrs={"type": "date"}),
            "componentes_a_evaluar": forms.SelectMultiple(attrs={"size": 10}),
            "observaciones": forms.Textarea(attrs={"rows": 2}),
        }
