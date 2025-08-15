from rest_framework import serializers

from .models import StockCategory, StockItem


class StockCategorySerializer(serializers.ModelSerializer):
    """Serializer for StockCategory model."""

    class Meta:
        model = StockCategory
        fields = ["id", "name", "description", "bootstrap_icon", "is_active"]


class StockItemSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for StockItem model."""

    category = serializers.HyperlinkedRelatedField(
        view_name="stockcategory-detail", queryset=StockCategory.objects.all()
    )
    current_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    available_quantity = serializers.IntegerField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.DecimalField(
        max_digits=5, decimal_places=2, read_only=True
    )

    class Meta:
        model = StockItem
        fields = [
            "url",
            "name",
            "description",
            "bootstrap_icon",
            "category",
            "original_price",
            "discount",
            "current_price",
            "discount_percentage",
            "quantity",
            "reserved_quantity",
            "available_quantity",
            "low_stock_threshold",
            "min_order_quantity",
            "max_order_quantity",
            "is_active",
            "is_featured",
            "is_in_stock",
            "is_low_stock",
        ]
