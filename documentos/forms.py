from django import forms
from .models import DocumentoSoporte, EvidenciaEjecucion


class DocumentoSoporteForm(forms.ModelForm):
    class Meta:
        model = DocumentoSoporte
        fields = ["archivo", "descripcion", "fecha_documento", "fecha_vigencia_hasta", "version"]
        widgets = {
            "fecha_documento": forms.DateInput(attrs={"type": "date"}),
            "fecha_vigencia_hasta": forms.DateInput(attrs={"type": "date"}),
        }


class EvidenciaEjecucionForm(forms.ModelForm):
    class Meta:
        model = EvidenciaEjecucion
        fields = ["tipo_archivo", "archivo", "descripcion", "fecha_evidencia", "auditoria"]
        widgets = {
            "fecha_evidencia": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, empresa=None, **kwargs):
        super().__init__(*args, **kwargs)
        if empresa is not None:
            self.fields["auditoria"].queryset = self.fields["auditoria"].queryset.filter(empresa=empresa)
        self.fields["auditoria"].required = False
