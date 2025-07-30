from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .setup_groups import AbstractGroupSetupCommand

User = get_user_model()


class Command(AbstractGroupSetupCommand):
    """
    Creates the ACCOUNTS_MANAGER group with appropriate permissions for user and group management.

    This command creates a group with full CRUD permissions for account-related models:
    - User: Add, Change, Delete, View
    - Group: Add, Change, Delete, View

    The command is idempotent - it can be run multiple times safely.

    Note: This gives powerful permissions to manage users and groups - assign carefully!
    """

    help = "Create ACCOUNTS_MANAGER group with user and group management permissions"

    groups_config = [
        {
            "name": "ACCOUNTS_MANAGER",
            "models_permissions": [
                (User, ["add", "change", "delete", "view"]),
                (Group, ["add", "change", "delete", "view"]),
            ],
            "description": "Full CRUD permissions for users and groups management",
        }
    ]

    def get_model_display_name(self, model_name):
        """Custom model name formatting for auth models."""
        name_mappings = {"user": "User", "group": "Group"}

        return name_mappings.get(model_name.lower(), model_name.title())

    def _print_usage_notes(self):
        """Print security warnings for accounts management."""
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("SECURITY NOTES")
        self.stdout.write("=" * 60)
        self.stdout.write(
            "⚠️  ACCOUNTS_MANAGER has powerful permissions - assign carefully!"
        )
        self.stdout.write("• Can create, modify, and delete user accounts")
        self.stdout.write("• Can create, modify, and delete permission groups")
        self.stdout.write(
            "• Consider using Django's built-in staff/superuser permissions instead"
        )
        self.stdout.write("• Only assign to trusted administrators")
