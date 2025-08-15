from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import StockCategoryViewSet, StockItemViewSet

router = DefaultRouter()
router.register(r"categories", StockCategoryViewSet, basename="stockcategory")
router.register(r"items", StockItemViewSet, basename="stockitem")

urlpatterns = [
    path("", include(router.urls)),
]
