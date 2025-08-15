from django.urls import path

from .adminsite import admin_site
from django.views.generic import RedirectView

urlpatterns = [
    path("portal/", admin_site.urls, name="admin:index"),
    path("", RedirectView.as_view(url="/portal/", permanent=False), name="index"),
]
