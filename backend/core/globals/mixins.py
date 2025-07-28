from django.conf import settings
from django.shortcuts import redirect


class AnonymousRequiredMixin:
    """
    Mixin that requires user to be anonymous (not authenticated).
    Redirects authenticated users to the registered login redirect URL.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_authenticated_redirect_url())
        return super().dispatch(request, *args, **kwargs)

    def get_authenticated_redirect_url(self):
        """
        Get the URL to redirect authenticated users to.
        Uses the registry's safe method with built-in fallbacks.
        """
        return settings.LOGIN_REDIRECT_URL


class UniqueChoiceFormMixin:
    """
    Mixin for forms that restricts the 'name' field choices to those not
    already used in the database, ensuring uniqueness.
    """

    choices_attr = "MODEL_CHOICES"  # Default attribute name for choices

    def __init__(self, *args, **kwargs):
        """
        Initializes the form and dynamically filters available 'name' choices
        based on which ones are not already used in the database.
        """
        super().__init__(*args, **kwargs)

        if self.instance.pk or not self.choices_attr:
            return

        model_choices = getattr(self._meta.model, self.choices_attr, [])
        existing_values = self._meta.model.objects.values_list("name", flat=True)

        available_choices = [
            choice for choice in model_choices if choice[0] not in existing_values
        ]

        self.fields["name"].choices = [(None, "")] + available_choices
