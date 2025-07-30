from core.accounts.management.commands.setup_groups import AbstractGroupSetupCommand

from ...models import Order


class Command(AbstractGroupSetupCommand):
    """
    Creates order management groups with appropriate permissions.

    This command creates two groups:
    1. ORDERS_MANAGER: Full management permissions for assigned orders, view permissions for unassigned orders
    2. ORDERS_HANDLER: View permissions for assigned orders only

    The command is idempotent - it can be run multiple times safely.

    Groups and permissions:
    - ORDERS_MANAGER:
      - Order: Change, Delete, View (base model permissions)

    - ORDERS_HANDLER:
      - Order: View, Change (base model permissions)
    """

    help = "Create order management groups with appropriate permissions"

    groups_config = [
        {
            "name": "ORDERS_MANAGER",
            "models_permissions": [
                (Order, ["change", "delete", "view"]),
            ],
            "description": "Full management permissions for orders",
        },
        {
            "name": "ORDERS_HANDLER",
            "models_permissions": [
                (Order, ["view", "change"]),
            ],
            "description": "View permissions for assigned orders",
        },
    ]

    def get_model_display_name(self, model_name):
        """Custom model name formatting for order models."""
        if model_name == "order":
            return "Order"
        return model_name.replace("order", "").title() or "Order"

    def _print_usage_notes(self):
        """Print custom usage notes for orders groups."""
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("USAGE NOTES")
        self.stdout.write("=" * 60)
        self.stdout.write(
            "• ORDERS_MANAGER: Can manage (change/delete/view) all orders and order items"
        )
        self.stdout.write("• ORDERS_HANDLER: Can only view orders and order items")
        self.stdout.write(
            "• Proxy models (AssignedOrder/UnassignedOrder) inherit permissions from Order model"
        )
        self.stdout.write(
            "• Use Django admin or custom views to filter proxy models appropriately"
        )
