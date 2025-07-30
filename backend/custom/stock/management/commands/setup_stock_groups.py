from core.accounts.management.commands.setup_groups import AbstractGroupSetupCommand

from ...models import StockCategory, StockItem


class Command(AbstractGroupSetupCommand):
    """
    Creates the STOCK_MANAGER group with appropriate permissions for stock management.

    This command creates a group with full CRUD permissions for StockCategory and StockItem models.
    The command is idempotent - it can be run multiple times safely.

    Permissions granted:
    - StockCategory: Add, Change, Delete, View
    - StockItem: Add, Change, Delete, View
    """

    help = "Create STOCK_MANAGER group with stock management permissions"

    groups_config = [
        {
            "name": "STOCK_MANAGER",
            "models_permissions": [
                (StockCategory, ["add", "change", "delete", "view"]),
                (StockItem, ["add", "change", "delete", "view"]),
            ],
            "description": "Full CRUD permissions for stock management",
        }
    ]

    def get_model_display_name(self, model_name):
        """Custom model name formatting for stock models."""
        return model_name.replace("stock", "").title()
