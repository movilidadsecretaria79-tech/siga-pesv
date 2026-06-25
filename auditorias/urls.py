from django.urls import path
from . import views

app_name = "auditorias"

urlpatterns = [
    path("", views.AuditoriaListView.as_view(), name="lista"),
    path("nueva/", views.AuditoriaCrearView.as_view(), name="crear"),
    path("<int:pk>/", views.AuditoriaDetailView.as_view(), name="detalle"),
    path("<int:pk>/checklist/guardar/", views.ChecklistGuardarView.as_view(), name="checklist_guardar"),
    path("<int:pk>/hallazgos/nuevo/", views.HallazgoCrearView.as_view(), name="hallazgo_crear"),
    path("<int:pk>/hallazgos/<int:hallazgo_id>/eliminar/", views.HallazgoEliminarView.as_view(), name="hallazgo_eliminar"),
    path("<int:pk>/hallazgos/<int:hallazgo_id>/acciones/nueva/", views.AccionMejoraCrearView.as_view(), name="accion_crear"),
    path("<int:pk>/acciones/<int:accion_id>/actualizar/", views.AccionMejoraActualizarView.as_view(), name="accion_actualizar"),
    path("<int:pk>/cerrar/", views.AuditoriaCerrarView.as_view(), name="cerrar"),
    path("<int:pk>/informe/", views.InformeAuditoriaView.as_view(), name="informe"),
]
