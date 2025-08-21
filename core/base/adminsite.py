from decouple import config
from django.contrib.admin import AdminSite as AbstractAdminSite
from django.utils.translation import gettext_lazy as _


class AdminSite(AbstractAdminSite):
    """
    Custom admin site for the organization.
    """

    site_name = config("SITE_NAME", default="").strip()
    site_header = _(f"{site_name} Admin Portal")
    site_title = _(f"{site_name} Admin Portal")
    index_title = _(f"Welcome to the {site_name} Admin Portal")


# Create custom admin site instance
admin_site = AdminSite(name="admin_site")
