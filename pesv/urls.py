from django.urls import path
from . import views

app_name = "pesv"

urlpatterns = [
    path("catalogo/", views.CatalogoPESVView.as_view(), name="catalogo"),
]
