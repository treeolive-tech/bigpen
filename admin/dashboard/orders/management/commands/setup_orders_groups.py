from django.contrib.auth import get_user_model

from dashboard.stock.models import StockCategory, StockItem
from home.accounts.management.commands.setup_groups import AbstractGroupSetupCommand

from ...models import Order, OrderItem

User = get_user_model()


class Command(AbstractGroupSetupCommand):
    help = "Create order management groups with appropriate permissions"

    groups_config = [
        {
            "id": 24,
            "name": "ORDERS_MANAGER",
            "models_permissions": [
                (Order, ["add", "change", "delete", "view"]),
                (OrderItem, ["add", "change", "delete", "view"]),
                (StockCategory, ["view"]),
                (StockItem, ["view"]),
                (User, ["view"]),
            ],
            "description": "Full management permissions for orders",
        },
        {
            "id": 25,
            "name": "ORDERS_OPERATOR",
            "models_permissions": [
                (Order, ["view", "change"]),
                (OrderItem, ["view"]),
                (StockCategory, ["view"]),
                (StockItem, ["view"]),
                (User, ["view"]),
            ],
            "description": "View and Modify (can only modify status e.g from pending to completed etc.) permissions for assigned orders",
        },
    ]

    def get_model_display_name(self, model_name):
        """Custom model name formatting for order models."""
        if model_name == "order":
            return "Order"
        return model_name.replace("order", "").title() or "Order"
