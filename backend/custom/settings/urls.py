from django.urls import include, path

urlpatterns = [
    path("", include("core.settings.urls")),
    # path("", include("custom..urls")),
]
