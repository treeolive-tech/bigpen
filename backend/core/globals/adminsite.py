from decouple import config
from django.conf import settings
from django.contrib.admin import AdminSite as AbstractAdminSite
from django.utils.translation import gettext_lazy as _


class AdminSite(AbstractAdminSite):
    """
    Custom admin site for the organization.
    """

    site_name = config("SITE_NAME", default="")
    site_header = _(f"{site_name} Admin")
    site_title = _(f"{site_name} Admin Portal")
    index_title = _(f"Welcome to the {site_name} Admin Portal")
    site_url = getattr(settings, "FRONTEND_WEB_URL", "/")

    # def get_urls(self):
    #     """
    #     Returns a list of URL patterns for the custom admin site.

    #     Adds custom login and logout paths (handled by `signin` and `signout` views),
    #     and appends the default admin site URLs.
    #     """
    #     from django.urls import path

    #     urls = super().get_urls()
    #     custom_urls = [
    #         path("login/", signin, name="admin_login"),
    #         path("logout/", signout, name="admin_logout"),
    #     ]
    #     return custom_urls + urls


# Create custom admin site instance
admin_site = AdminSite(name="admin_site")
