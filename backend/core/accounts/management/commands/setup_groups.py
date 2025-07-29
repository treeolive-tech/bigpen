from django.apps import apps
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
