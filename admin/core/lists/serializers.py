from rest_framework import serializers

from .models import ListCategory, ListItem


class ListCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ListCategory
        fields = [
            "url",
            "name",
        ]


class ListItemSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.HyperlinkedRelatedField(
        view_name="listcategory-detail", queryset=ListCategory.objects.all()
    )

    class Meta:
        model = ListItem
        fields = [
            "url",
            "name",
            "description",
            "bootstrap_icon",
            "category",
        ]
