from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as AbstractGroupAdmin
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin

from core.globals.adminsite import admin_site

from .forms import UserForm
from .models import Group, User


@admin.register(Group, site=admin_site)
class GroupAdmin(AbstractGroupAdmin):
    pass


@admin.register(User, site=admin_site)
class UserAdmin(AbstractUserAdmin):
    readonly_fields = ("is_staff", "is_superuser")
    form = UserForm

    def get_form(self, request, obj=None, **kwargs):
        """Override get_form to pass the current user to the form"""
        Form = super().get_form(request, obj, **kwargs)
        return Form

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        if request.user.is_superuser:
            return fieldsets

        # Hide sensitive fields for non-superusers
        fieldsets = list(fieldsets)
        for name, section in fieldsets:
            section["fields"] = tuple(
                field
                for field in section["fields"]
                if field not in ["is_staff", "is_superuser", "user_permissions"]
            )

        return fieldsets
