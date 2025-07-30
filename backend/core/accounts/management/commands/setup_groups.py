from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django management command that automatically discovers and executes app-specific group setup commands.

    This command iterates through all INSTALLED_APPS, extracts their app labels, and attempts to call
    corresponding setup_[app_label]_groups management commands. It provides comprehensive reporting
    and filtering options.

    Key Features:
    - Automatic Discovery: Checks all INSTALLED_APPS for setup_[app_label]_groups commands
    - Dry Run Mode: Preview what would be executed without actually running commands
    - App Filtering: Run only specific apps or exclude certain apps
    - Comprehensive Reporting: Shows found, executed, failed, and missing commands

    Usage Examples:
    - python manage.py setup_groups --dry-run
    - python manage.py setup_groups
    - python manage.py setup_groups --apps users products orders
    - python manage.py setup_groups --exclude django_admin auth contenttypes

    For this command to work, individual apps should have their own group setup commands:
    - users/management/commands/setup_users_groups.py
    - products/management/commands/setup_products_groups.py
    - etc.
    """

    help = "Setup groups for all apps that have setup_[app_label]_groups commands"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show which commands would be executed without actually running them",
        )
        parser.add_argument(
            "--apps",
            nargs="+",
            help="Only run setup for specific app labels (space-separated)",
        )
        parser.add_argument(
            "--exclude",
            nargs="+",
            help="Exclude specific app labels from setup (space-separated)",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        specific_apps = options.get("apps")
        excluded_apps = options.get("excluded_apps", [])

        if dry_run:
            self.stdout.write(
                self.style.WARNING("DRY RUN MODE - No commands will be executed")
            )

        # Get all installed apps
        installed_apps = apps.get_app_configs()

        # Filter apps if specific ones are requested
        if specific_apps:
            installed_apps = [
                app for app in installed_apps if app.label in specific_apps
            ]

        # Exclude specified apps
        if excluded_apps:
            installed_apps = [
                app for app in installed_apps if app.label not in excluded_apps
            ]

        commands_found = []
        commands_not_found = []
        commands_executed = []
        commands_failed = []

        for app_config in installed_apps:
            app_label = app_config.label
            command_name = f"setup_{app_label}_groups"

            if self._command_exists(command_name):
                commands_found.append((app_label, command_name))

                if dry_run:
                    self.stdout.write(self.style.SUCCESS(f"  ✓ Found: {command_name}"))
                else:
                    try:
                        self.stdout.write(
                            self.style.SUCCESS(f"  ✓ Executing: {command_name}")
                        )
                        call_command(command_name)
                        commands_executed.append((app_label, command_name))
                        self.stdout.write(
                            self.style.SUCCESS(f"  ✓ Completed: {command_name}")
                        )
                    except Exception as e:
                        commands_failed.append((app_label, command_name, str(e)))
                        self.stdout.write(
                            self.style.ERROR(f"  ✗ Failed: {command_name} - {e}")
                        )
            else:
                commands_not_found.append((app_label, command_name))
                if dry_run:
                    self.stdout.write(
                        self.style.WARNING(f"  - Not found: {command_name}")
                    )

        # Summary
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("SUMMARY"))
        self.stdout.write("=" * 50)

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"Commands that would be executed: {len(commands_found)}"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Commands executed successfully: {len(commands_executed)}"
                )
            )
            if commands_failed:
                self.stdout.write(
                    self.style.ERROR(f"Commands failed: {len(commands_failed)}")
                )

        self.stdout.write(f"Commands not found: {len(commands_not_found)}")

        # Detailed summary
        if commands_found:
            self.stdout.write("\nCommands found:")
            for app_label, command_name in commands_found:
                status = "WOULD EXECUTE" if dry_run else "EXECUTED"
                self.stdout.write(f"  - {app_label}: {command_name} ({status})")

        if commands_failed:
            self.stdout.write("\nCommands failed:")
            for app_label, command_name, error in commands_failed:
                self.stdout.write(f"  - {app_label}: {command_name} - {error}")

        if commands_not_found and dry_run:
            self.stdout.write("\nCommands not found:")
            for app_label, command_name in commands_not_found:
                self.stdout.write(f"  - {app_label}: {command_name}")

    def _command_exists(self, command_name):
        """
        Check if a management command exists.
        """
        try:
            from django.core.management import get_commands

            commands = get_commands()
            return command_name in commands
        except Exception:
            return False


class AbstractGroupSetupCommand(BaseCommand):
    """
    Base class for Django management commands that create groups with permissions.

    Subclasses should define:
    - groups_config: List of dictionaries with group configuration
    - help: Help text for the command
    - Optional: get_model_display_name() method for custom model name formatting
    """

    groups_config = []  # Override in subclasses

    def handle(self, *args, **options):
        if not self.groups_config:
            self.stdout.write(
                self.style.ERROR("No groups configuration defined in subclass")
            )
            return

        self.stdout.write("Setting up groups...")

        total_permissions_added = 0
        total_permissions_existed = 0

        for group_config in self.groups_config:
            permissions_added, permissions_existed = self._setup_group(group_config)
            total_permissions_added += permissions_added
            total_permissions_existed += permissions_existed

        self._print_final_summary(total_permissions_added, total_permissions_existed)

    def _setup_group(self, group_config):
        """Set up a single group with its permissions."""
        group_name = group_config["name"]
        models_permissions = group_config["models_permissions"]
        description = group_config.get("description", "")

        self._print_group_header(group_name)

        # Create or get the group
        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Created {group_name} group"))
        else:
            self.stdout.write(
                self.style.WARNING(f"→ {group_name} group already exists")
            )

        permissions_added = 0
        permissions_already_existed = 0

        # Add permissions to the group
        for model, permission_codenames in models_permissions:
            added, existed = self._process_model_permissions(
                group, model, permission_codenames
            )
            permissions_added += added
            permissions_already_existed += existed

        self._print_group_summary(
            group_name,
            description,
            permissions_added,
            permissions_already_existed,
            group.permissions.count(),
        )

        return permissions_added, permissions_already_existed

    def _process_model_permissions(self, group, model, permission_codenames):
        """Process permissions for a single model."""
        content_type = ContentType.objects.get_for_model(model)
        model_name = model._meta.model_name

        self.stdout.write(f"\nProcessing {model.__name__} permissions:")

        permissions_added = 0
        permissions_already_existed = 0

        for codename in permission_codenames:
            perm_codename = f"{codename}_{model_name}"

            try:
                permission = Permission.objects.get(
                    codename=perm_codename, content_type=content_type
                )

                if group.permissions.filter(id=permission.id).exists():
                    self.stdout.write(
                        f"  → {codename.title()} permission already exists"
                    )
                    permissions_already_existed += 1
                else:
                    group.permissions.add(permission)
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✓ Added {codename.title()} permission")
                    )
                    permissions_added += 1

            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"  ✗ Permission {perm_codename} not found")
                )

        return permissions_added, permissions_already_existed

    def _print_group_header(self, group_name):
        """Print header for group setup section."""
        if len(self.groups_config) > 1:
            self.stdout.write(f"\n{'=' * 60}")
            self.stdout.write(f"Setting up {group_name}")
            self.stdout.write(f"{'=' * 60}")

    def _print_group_summary(self, group_name, description, added, existed, total):
        """Print summary for a single group."""
        if len(self.groups_config) > 1:
            self.stdout.write(f"\n{group_name} Summary:")
            if description:
                self.stdout.write(f"  Description: {description}")
            self.stdout.write(f"  Permissions added: {added}")
            self.stdout.write(f"  Permissions already existed: {existed}")
            self.stdout.write(f"  Total permissions in group: {total}")

    def _print_final_summary(self, total_added, total_existed):
        """Print the final summary of all operations."""
        separator = "=" * (60 if len(self.groups_config) > 1 else 50)

        self.stdout.write(f"\n{separator}")
        self.stdout.write(self.style.SUCCESS("SETUP COMPLETE"))
        self.stdout.write(separator)

        if len(self.groups_config) == 1:
            # Single group format (like stock groups)
            group_config = self.groups_config[0]
            group_name = group_config["name"]
            group = Group.objects.get(name=group_name)

            self.stdout.write(f"Group: {group_name}")
            self.stdout.write(f"Permissions added: {total_added}")
            self.stdout.write(f"Permissions already existed: {total_existed}")
            self.stdout.write(f"Total permissions: {group.permissions.count()}")

            self._print_group_permissions(group)

        else:
            # Multiple groups format (like orders groups)
            self.stdout.write("Groups created:")
            for group_config in self.groups_config:
                group_name = group_config["name"]
                group = Group.objects.get(name=group_name)
                self.stdout.write(
                    f"  • {group_name} ({group.permissions.count()} permissions)"
                )

            self.stdout.write(f"\nTotal permissions added: {total_added}")
            self.stdout.write(f"Total permissions already existed: {total_existed}")

            # List permissions for each group
            for group_config in self.groups_config:
                group_name = group_config["name"]
                group = Group.objects.get(name=group_name)
                self.stdout.write(f"\n{group_name} permissions:")
                self._print_group_permissions(group, indent="  ")

        self._print_success_message()
        self._print_usage_notes()

    def _print_group_permissions(self, group, indent=""):
        """Print all permissions for a group."""
        if len(self.groups_config) == 1:
            self.stdout.write("\nCurrent group permissions:")
            indent = "  "

        for perm in group.permissions.all().order_by("content_type__model", "codename"):
            model_name = self.get_model_display_name(perm.content_type.model)
            action = perm.codename.split("_")[0].title()
            self.stdout.write(f"{indent}• {model_name}: {action}")

    def get_model_display_name(self, model_name):
        """
        Get display name for a model. Override in subclasses for custom formatting.

        Args:
            model_name: The model name from content_type.model

        Returns:
            Formatted model name for display
        """
        return model_name.title()

    def _print_success_message(self):
        """Print the final success message. Override in subclasses if needed."""
        if len(self.groups_config) == 1:
            group_name = self.groups_config[0]["name"]
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✓ {group_name} group setup completed successfully!"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("\n✓ Groups setup completed successfully!")
            )

    def _print_usage_notes(self):
        """Print usage notes. Override in subclasses to add custom notes."""
        pass
