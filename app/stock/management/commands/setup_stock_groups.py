from olyv.accounts.management.commands.setup_groups import AbstractGroupSetupCommand

from ...models import StockCategory, StockItem


class Command(AbstractGroupSetupCommand):
    """
    Creates stock management groups with appropriate permissions:

    STOCK_OPERATOR:
    - Stock Categories: View only (cannot create or modify categories)
    - Stock Items: Full CRUD (can add, edit, delete, and view items)

    STOCK_MANAGER:
    - Stock Categories: Full CRUD (can manage all categories)
    - Stock Items: Full CRUD (can manage all items)

    The command is idempotent - it can be run multiple times safely.
    """

    help = "Create STOCK_OPERATOR and STOCK_MANAGER groups with appropriate stock management permissions"

    groups_config = [
        {
            "id": 26,
            "name": "STOCK_OPERATOR",
            "models_permissions": [
                (StockCategory, ["view"]),  # View-only access to categories
                (
                    StockItem,
                    ["add", "change", "delete", "view"],
                ),  # Full access to items
            ],
            "description": (
                "Operators can fully manage stock items (create, edit, delete), "
                "but can only view stock categories. Category management is reserved for STOCK_MANAGER group."
            ),
        },
        {
            "id": 27,
            "name": "STOCK_MANAGER",
            "models_permissions": [
                (
                    StockCategory,
                    ["add", "change", "delete", "view"],
                ),  # Full category management
                (
                    StockItem,
                    ["add", "change", "delete", "view"],
                ),  # Full item management
            ],
            "description": ("Full management permissions for all stock categories and items."),
        },
    ]

    def get_model_display_name(self, model_name):
        """Custom model name formatting for stock models."""
        name_mappings = {
            "stockcategory": "Stock Category",
            "stockitem": "Stock Item",
        }
        return name_mappings.get(model_name.lower(), model_name.title())
