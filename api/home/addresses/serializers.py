from rest_framework.serializers import HyperlinkedModelSerializer

from .models import EmailAddress, PhoneAddress, PhysicalAddress, SocialMediaAddress


class EmailAddressSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = EmailAddress
        fields = ["url", "email", "is_primary", "mailto_link"]


class PhoneAddressSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = PhoneAddress
        fields = [
            "url",
            "number",
            "is_primary",
            "use_for_whatsapp",
            "is_active",
            "formatted_number",
            "national_format",
            "international_format",
            "tel_link",
            "whatsapp_link",
        ]

    def to_representation(self, instance):
        # Only include the whatsapp_link field if use_for_whatsapp is True.
        data = super().to_representation(instance)
        if not data.get("use_for_whatsapp"):
            data.pop("whatsapp_link", None)
        return data


class PhysicalAddressSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = PhysicalAddress
        fields = [
            "url",
            "label",
            "building",
            "street_address",
            "city",
            "state_province",
            "postal_code",
            "country",
            "map_embed_url",
            "use_in_contact_form",
            "is_active",
            "full_address",
            "short_address",
            "google_maps_url",
        ]


class SocialMediaAddressSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = SocialMediaAddress
        fields = [
            "url",
            "name",
            "icon",
            "url",
            "is_active",
            "display_name",
            "icon_html",
        ]
