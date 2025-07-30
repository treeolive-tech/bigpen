from core.accounts.management.commands.setup_groups import AbstractGroupSetupCommand

from ...models import Article, ArticleCategory, ArticleTag


class Command(AbstractGroupSetupCommand):
    """
    Creates the ARTICLES_AUTHOR group with appropriate permissions for article management.

    This command creates a group with full CRUD permissions for article-related models:
    - ArticleCategory: Add, Change, Delete, View
    - ArticleTag: Add, Change, Delete, View
    - Article: Add, Change, Delete, View

    The command is idempotent - it can be run multiple times safely.
    """

    help = "Create ARTICLES_AUTHOR group with article management permissions"

    groups_config = [
        {
            "name": "ARTICLES_AUTHOR",
            "models_permissions": [
                (ArticleCategory, ["add", "change", "delete", "view"]),
                (ArticleTag, ["add", "change", "delete", "view"]),
                (Article, ["add", "change", "delete", "view"]),
            ],
            "description": "Full CRUD permissions for articles, categories, and tags",
        }
    ]

    def get_model_display_name(self, model_name):
        """Custom model name formatting for article models."""
        name_mappings = {
            "articlecategory": "Article Category",
            "articletag": "Article Tag",
            "article": "Article",
        }

        return name_mappings.get(model_name.lower(), model_name.title())
