from django.urls import path
from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("matriz-seguimiento/", views.MatrizSeguimientoView.as_view(), name="matriz"),
]
