from core.globals.models import AbstractDisplayOrder
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as ProxiedGroup
from django.db import models


class Group(ProxiedGroup):
    class Meta:
        proxy = True
        verbose_name = "Group"
        verbose_name_plural = "Groups"


class User(AbstractUser, AbstractDisplayOrder):
    """Custom User model with group-based permissions and staff status management"""

    # 👇make email optional
    email = models.EmailField(blank=True, null=True)
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "auth_user"
        ordering = ["display_order", "username"]
