from django.urls import path
from django.views.generic import RedirectView

from .adminsite import admin_site

urlpatterns = [
    path("admin/", admin_site.urls, name="admin:index"),
    path("", RedirectView.as_view(url="/admin/", permanent=False), name="index"),
]
