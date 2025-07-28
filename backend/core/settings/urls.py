from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("", admin.site.urls),
]

admin.site.site_header = f"{settings.SITE_NAME} Admin"
admin.site.site_title = f"{settings.SITE_NAME} Admin Portal"
admin.site.index_title = f"Welcome to the {settings.SITE_NAME} Admin Portal"


if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
