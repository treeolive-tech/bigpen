from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


class OrderItemFormSet(BaseInlineFormSet):
    def clean(self):
        """Validate that at least one item remains after deletions and completion rules."""
        super().clean()

        if any(self.errors):
            return

        # Count non-deleted forms with data
        valid_forms = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                valid_forms += 1

        if valid_forms == 0:
            raise ValidationError(
                "An order must have at least one item. If you want to remove all items, please delete the order instead."
            )

        # Check if items are being marked as completed by the assigned user
        if hasattr(self, "instance") and self.instance.pk:
            current_user = self.request.user if hasattr(self, "request") else None
            for form in self.forms:
                if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                    is_completed = form.cleaned_data.get("is_completed", False)
                    was_completed = (
                        form.instance.is_completed if form.instance.pk else False
                    )

                    # Only validate if trying to mark as completed
                    if is_completed and not was_completed:
                        if not self.instance.is_assigned:
                            raise ValidationError(
                                "Cannot mark items as completed. The order must be assigned to a staff member first."
                            )
                        if current_user != self.instance.staff_orders_handler:
                            raise ValidationError(
                                "Only the assigned staff member can mark items as completed."
                            )
