from django.urls import path
from . import views

app_name = "programa"

urlpatterns = [
    path("", views.ProgramaListView.as_view(), name="lista"),
    path("nuevo/", views.ProgramaCreateView.as_view(), name="crear"),
    path("<int:pk>/", views.ProgramaDetailView.as_view(), name="detalle"),
    path("<int:pk>/editar/", views.ProgramaUpdateView.as_view(), name="editar"),
    path("<int:programa_id>/visitas/nueva/", views.VisitaCreateView.as_view(), name="visita_crear"),
    path("visitas/<int:pk>/editar/", views.VisitaUpdateView.as_view(), name="visita_editar"),
]
