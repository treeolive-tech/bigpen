from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("", include("core.globals.urls")),
    path("addresses/", include("core.addresses.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += [
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
