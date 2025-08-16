from django import forms

from home.globals.mixins import UniqueChoiceFormMixin

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


class EmailUsForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(min_length=10)

    def clean_message(self):
        message = self.cleaned_data.get("message", "")
        if len(message.strip()) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message
