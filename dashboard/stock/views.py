from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .models import StockCategory, StockItem
from .serializers import StockCategorySerializer, StockItemSerializer


class StockCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockCategory.objects.all()
    serializer_class = StockCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_active"]


class StockItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_active", "category"]