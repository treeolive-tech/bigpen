import traceback
from pathlib import Path

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    A Django management command to load multiple fixture files at once.

    This command provides flexible options for loading fixtures:
    1. Load from a specific directory
    2. Load from a specific app's fixtures directory
    3. Load from all apps' fixtures directories

    Usage:
        # Load from specific directory
        python manage.py loadfixtures path/to/fixtures

        # Load from specific app's fixtures directory
        python manage.py loadfixtures --app_label=myapp

        # Load all fixtures from all apps
        python manage.py loadfixtures

        # With verbose output
        python manage.py loadfixtures --verbose

        # Load YAML fixtures from an app
        python manage.py loadfixtures --app_label=myapp --extension=yaml

    Note:
        - Fixtures are loaded in alphabetical order
        - The command will stop on the first error encountered
        - Use --verbose flag to see detailed loading progress
    """

    help = "Load all fixture files from a specified directory or from app's fixtures directories"

    def add_arguments(self, parser):
        """
        Define the command line arguments.

        Arguments:
            fixture_dir: Optional path to directory containing fixtures
            --extension: File extension to look for (defaults to 'json')
            --app_label: App label to load fixtures from a specific app
            --verbose: Flag to show detailed loading progress
        """
        parser.add_argument(
            "fixture_dir",
            type=str,
            nargs="?",
            default=None,
            help="Directory containing the fixtures",
        )
        parser.add_argument(
            "--extension",
            default="json",
            help="File extension to look for (default: json)",
        )
        parser.add_argument(
            "--app_label",
            type=str,
            help="App label to load fixtures from a specific app",
        )
        parser.add_argument(
            "--verbose", action="store_true", help="Show verbose output"
        )

    def handle(self, *args, **options):
        """
        Execute the command to load fixtures.

        The command follows this process:
        1. Determine the source of fixtures (specific dir, app dir, or all apps)
        2. Find all matching fixture files
        3. Sort files alphabetically
        4. Load each fixture in order

        If --verbose is set, provides detailed progress information.
        Stops on the first error encountered.
        """
        fixture_dir = options["fixture_dir"]
        extension = options["extension"]
        app_label = options["app_label"]
        verbose = options["verbose"]

        fixture_files = []

        # Case 1: Loading from a specific directory
        if fixture_dir:
            fixture_path = Path(fixture_dir).resolve()
            if not fixture_path.exists():
                self.stderr.write(
                    self.style.ERROR(f"Directory not found: {fixture_dir}")
                )
                return

            fixture_files = [
                f for f in fixture_path.rglob(f"*.{extension}") if f.name != "seed_example.json"
            ]

        # Case 2: Loading from app fixtures directories
        else:
            if app_label:
                # Load from specific app's fixtures directory
                try:
                    app_config = apps.get_app_config(app_label)
                    app_fixtures_path = Path(app_config.path) / "fixtures"
                    fixture_files = [
                        f
                        for f in app_fixtures_path.rglob(f"*.{extension}")
                        if f.name != "seed_example.json"
                    ]
                except LookupError:
                    self.stderr.write(self.style.ERROR(f"App '{app_label}' not found"))
                    return
            else:
                # Load from all apps' fixtures directories
                for app_config in apps.get_app_configs():
                    app_fixtures_path = Path(app_config.path) / "fixtures"
                    fixture_files.extend(
                        [
                            f
                            for f in app_fixtures_path.rglob(f"*.{extension}")
                            if f.name != "seed_example.json"
                        ]
                    )

        if verbose:
            self.stdout.write(f"Search pattern: *.{extension}")

        if not fixture_files:
            self.stderr.write(
                self.style.WARNING(
                    f"No .{extension} files found in {fixture_dir or 'app fixtures directories'}"
                )
            )
            return

        # Sort files to ensure consistent loading order
        fixture_files.sort()

        if verbose:
            self.stdout.write(
                self.style.SUCCESS(f"Found {len(fixture_files)} fixture files:")
            )
            for file in fixture_files:
                self.stdout.write(f"  - {file.name}")

        # Load each fixture
        for fixture_file in fixture_files:
            try:
                if verbose:
                    self.stdout.write(f"Loading fixture: {fixture_file.name}...")
                call_command("loaddata", str(fixture_file))
                if verbose:
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfully loaded {fixture_file.name}")
                    )
            except Exception as e:
                error_message = "".join(
                    traceback.format_exception(None, e, e.__traceback__)
                )
                self.stderr.write(
                    self.style.ERROR(
                        f"Error loading {fixture_file.name}:\n{error_message}"
                    )
                )
                return

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully loaded all fixtures from {fixture_dir or 'app fixtures directories'}"
            )
        )
