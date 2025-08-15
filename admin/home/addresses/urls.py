from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    EmailAddressViewSet,
    EmailUsAPIView,
    PhoneAddressViewSet,
    PhysicalAddressViewSet,
    SocialMediaAddressViewSet,
)

router = DefaultRouter()
router.register(r"email", EmailAddressViewSet)
router.register(r"phone", PhoneAddressViewSet)
router.register(r"physical", PhysicalAddressViewSet)
router.register(r"social", SocialMediaAddressViewSet)

urlpatterns = [
    path("email-us/", EmailUsAPIView.as_view(), name="email-us"),
    path("", include(router.urls)),
]
