from django.urls import path
from . import views

app_name = "empresas"

urlpatterns = [
    path("", views.EmpresaListView.as_view(), name="lista"),
    path("nueva/", views.EmpresaCreateView.as_view(), name="crear"),
    path("<int:pk>/", views.EmpresaDetailView.as_view(), name="detalle"),
    path("<int:pk>/editar/", views.EmpresaUpdateView.as_view(), name="editar"),

    path("<int:empresa_id>/vehiculos/nuevo/", views.VehiculoCreateView.as_view(), name="vehiculo_crear"),
    path("vehiculos/<int:pk>/editar/", views.VehiculoUpdateView.as_view(), name="vehiculo_editar"),

    path("<int:empresa_id>/conductores/nuevo/", views.ConductorCreateView.as_view(), name="conductor_crear"),
    path("conductores/<int:pk>/", views.ConductorDetailView.as_view(), name="conductor_detalle"),
    path("conductores/<int:pk>/editar/", views.ConductorUpdateView.as_view(), name="conductor_editar"),
]
