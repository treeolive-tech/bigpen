from rest_framework import serializers

from .models import StockCategory, StockItem


class CategoryListSerializer(serializers.HyperlinkedModelSerializer):
    """Lightweight serializer for category list view"""

    item_count = serializers.SerializerMethodField()

    class Meta:
        model = StockCategory
        fields = [
            "url",
            "id",
            "name",
            "image",
            "bootstrap_icon",
            "is_active",
            "item_count",
        ]

    def get_item_count(self, obj):
        return obj.get_active_items().count()


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for category detail view"""

    active_items = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = StockCategory
        fields = [
            "id",
            "name",
            "description",
            "image",
            "bootstrap_icon",
            "is_active",
            "order",
            "created_at",
            "updated_at",
            "active_items",
            "total_items",
        ]

    def get_active_items(self, obj):
        from .serializers import ItemListSerializer

        items = obj.get_active_items()[:10]  # Limit to 10 items
        return ItemListSerializer(items, many=True, context=self.context).data

    def get_total_items(self, obj):
        return obj.items.count()


class ItemListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for item list view"""

    category_name = serializers.CharField(source="category.name", read_only=True)
    current_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    is_in_stock = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.DecimalField(
        max_digits=5, decimal_places=2, read_only=True
    )

    class Meta:
        model = StockItem
        fields = [
            "id",
            "name",
            "main_image",
            "category_name",
            "original_price",
            "current_price",
            "discount_percentage",
            "is_featured",
            "is_in_stock",
            "available_quantity",
            "bootstrap_icon",
        ]
