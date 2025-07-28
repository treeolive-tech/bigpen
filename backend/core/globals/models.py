from django.db import models


class AbstractDisplayOrder(models.Model):
    display_order = models.PositiveIntegerField(
        default=1,
        help_text="Display order (lower numbers - zero included - appear first)",
    )

    class Meta:
        abstract = True


class AbstractBootstrapIcon(models.Model):
    bootstrap_icon = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional. Bootstrap icon class or path for the item. Example: 'bi bi-cart' for a shopping cart icon. Find icons at [Bootstrap Icons](https://icons.getbootstrap.com/).",
    )

    class Meta:
        abstract = True


class AbstractCreatedUpdatedAt(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date and time created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time last updated.",
    )

    class Meta:
        abstract = True
