from django import forms

from core.globals.mixins import UniqueChoiceFormMixin

from .models import SocialMediaAddress


class SocialMediaAddressForm(UniqueChoiceFormMixin, forms.ModelForm):
    """
    Form for SocialMediaAddress model, filtering out existing choices for 'name'.
    Excludes the 'icon' field from the form.
    """

    class Meta:
        model = SocialMediaAddress
        fields = "__all__"
        exclude = ("icon",)
