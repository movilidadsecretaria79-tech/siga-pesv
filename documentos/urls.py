from django.urls import path
from . import views

app_name = "documentos"

urlpatterns = [
    path("empresa/<int:empresa_id>/", views.VerificacionRequisitosView.as_view(), name="verificacion_requisitos"),
    path("empresa/<int:empresa_id>/componente/<int:componente_id>/documento/subir/", views.DocumentoSoporteSubirView.as_view(), name="documento_subir"),
    path("empresa/<int:empresa_id>/componente/<int:componente_id>/evidencia/subir/", views.EvidenciaSubirView.as_view(), name="evidencia_subir"),
    path("empresa/<int:empresa_id>/componente/<int:componente_id>/historial/", views.ComponenteEvidenciasView.as_view(), name="componente_evidencias"),
]
