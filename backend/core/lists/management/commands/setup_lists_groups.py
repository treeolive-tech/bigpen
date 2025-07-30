from core.accounts.management.commands.setup_groups import AbstractGroupSetupCommand

from ...models import ListCategory, ListItem


class Command(AbstractGroupSetupCommand):
    """
    Creates the LISTS_MANAGER group with appropriate permissions for list management.

    This command creates a group with full CRUD permissions for list-related models:
    - ListCategory: Add, Change, Delete, View
    - ListItem: Add, Change, Delete, View

    The command is idempotent - it can be run multiple times safely.
    """

    help = "Create LISTS_MANAGER group with list management permissions"

    groups_config = [
        {
            "name": "LISTS_MANAGER",
            "models_permissions": [
                (ListCategory, ["add", "change", "delete", "view"]),
                (ListItem, ["add", "change", "delete", "view"]),
            ],
            "description": "Full CRUD permissions for list categories and items",
        }
    ]

    def get_model_display_name(self, model_name):
        """Custom model name formatting for list models."""
        name_mappings = {"listcategory": "List Category", "listitem": "List Item"}

        return name_mappings.get(model_name.lower(), model_name.title())
