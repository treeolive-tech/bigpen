from decouple import config
from django import template
from django.template import Context
from django.templatetags.static import static
from django.utils.safestring import SafeString, mark_safe

register = template.Library()


@register.simple_tag
def get_env(env_value: str) -> str:
    """
    Get site configuration values from environment variables with optional static file defaults.

    Retrieves any environment variable value. For common site assets, provides fallback
    to default static file paths if the environment variable is not set. For other
    environment variables, returns the value as-is or empty string if not found.

    Args:
        env_value: The environment variable name to look up. Common site asset variables
                  with static file defaults include:
                  - "SITE_LOGO": Site logo image
                  - "SITE_FAVICON": Site favicon
                  - "SITE_APPLE_TOUCH_ICON": Apple touch icon
                  - "SITE_ANDROID_CHROME_ICON": Android chrome icon
                  - "SITE_MS_TILE": Microsoft tile icon
                  - "SITE_HERO_1": Hero image 1

                  Any other environment variable can also be retrieved (e.g., "SITE_NAME",
                  "DEBUG", etc.) but will use empty string as default.

    Returns:
        The environment variable value stripped of whitespace. For asset variables,
        returns default static file path if env var is not set. For other variables,
        returns empty string if not found.

    Usage:
        {% get_env "SITE_LOGO" %}        ← returns env value or static default
        {% get_env "SITE_NAME" %}         ← returns env value or empty string
        {% get_env "DEBUG" %}             ← returns env value or empty string
    """
    match env_value:
        case "SITE_LOGO":
            default = static("base/globals/logo.png")
        case "SITE_FAVICON":
            default = static("base/globals/favicon.ico")
        case "SITE_APPLE_TOUCH_ICON":
            default = static("base/globals/apple-touch-icon.png")
        case "SITE_ANDROID_CHROME_ICON":
            default = static("base/globals/android-chrome-icon.png")
        case "SITE_MS_TILE":
            default = static("base/globals/mstile.png")
        case "SITE_HERO_1":
            default = static("base/sections/hero-1.jpg")
        case _:
            default = ""

    return config(env_value, default=default).strip()


@register.simple_tag(takes_context=True)
def title(context: Context, title: str = None, separator: str = " | ") -> SafeString:
    """
    Generate a complete HTML `<title>` tag combining page title and site name.

    Creates a properly formatted `<title>` element that combines a page-specific
    title with the site name from environment configuration. The title follows
    the pattern: "Page Title | Site Name" or just "Site Name" if no page title.

    Args:
        context: Django template context (automatically passed)
        title: Optional page title. If not provided, uses context['page_title']
        separator: String to separate page title and site name (default: " | ")

    Returns:
        SafeString containing the complete HTML `<title>` tag

    Usage:
        {% title %}                        ← "Site Name" or "Page Title | Site Name"
        {% title "Custom Page" %}          ← "Custom Page | Site Name"
        {% title "Custom Page" " - " %}    ← "Custom Page - Site Name"
        {% title separator=" :: " %}       ← "Page Title :: Site Name"

    Note:
        Requires SITE_NAME environment variable to be set for the site name portion.
    """
    site_name = config("SITE_NAME", default="").strip()
    title = title or context.get("page_title")

    full_title = f"{title}{separator}{site_name}" if title else site_name
    return mark_safe(f"<title>{full_title}</title>")
