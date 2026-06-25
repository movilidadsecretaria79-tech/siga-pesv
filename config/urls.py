from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("seguimiento.urls")),
    path("empresas/", include("empresas.urls")),
    path("pesv/", include("pesv.urls")),
    path("documentos/", include("documentos.urls")),
    path("programa/", include("programa.urls")),
    path("auditorias/", include("auditorias.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
