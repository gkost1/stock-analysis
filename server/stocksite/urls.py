from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("core/", include("core.urls")),
    path("simulations/", include("simulations.urls")),
]
