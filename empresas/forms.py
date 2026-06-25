from django import forms
from .models import Empresa, Vehiculo, Conductor


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        exclude = ["creado_en", "actualizado_en"]
        widgets = {
            "observaciones": forms.Textarea(attrs={"rows": 3}),
            "soat_vigencia": forms.DateInput(attrs={"type": "date"}),
        }


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        exclude = []
        widgets = {
            "soat_vigencia": forms.DateInput(attrs={"type": "date"}),
            "rtm_vigencia": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 2}),
        }


class ConductorForm(forms.ModelForm):
    class Meta:
        model = Conductor
        exclude = ["creado_en", "actualizado_en"]
        widgets = {
            "licencia_vigencia": forms.DateInput(attrs={"type": "date"}),
            "examen_medico_fecha": forms.DateInput(attrs={"type": "date"}),
            "examen_medico_vigencia": forms.DateInput(attrs={"type": "date"}),
            "comparendos_fecha_verificacion": forms.DateInput(attrs={"type": "date"}),
            "competencias_fecha_evaluacion": forms.DateInput(attrs={"type": "date"}),
            "comparendos_observaciones": forms.Textarea(attrs={"rows": 2}),
            "fatiga_controles_aplicados": forms.Textarea(attrs={"rows": 2}),
            "detalle_reincidencia": forms.Textarea(attrs={"rows": 2}),
            "plan_seguimiento_reincidencia": forms.Textarea(attrs={"rows": 2}),
        }
