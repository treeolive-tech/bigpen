from decouple import config
from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def base(env_value):
    match env_value:
        case "SITE_LOGO":
            default = static("base/images/logo.png")
        case "SITE_FAVICON":
            default = static("base/images/favicon.ico")
        case "SITE_APPLE_TOUCH_ICON":
            default = static("base/images/apple-touch-icon.png")
        case "SITE_ANDROID_CHROME_ICON":
            default = static("base/images/android-chrome-icon.png")
        case "SITE_MS_TILE":
            default = static("base/images/mstile.png")
        case _:
            default = ""

    return config(env_value, default=default).strip()


@register.simple_tag(takes_context=True)
def base_title(context, title=None, separator=" | "):
    """
    Render the full HTML <title> tag with the page title and site name.
    Usage:
      - {% base_title %}                   ← uses context['page_title']
      - {% base_title "Custom Title" %}    ← uses provided title
      - {% base_title "Custom" " - " %}    ← uses custom separator
    """
    site_name = config("SITE_NAME", default="").strip()
    title = title or context.get("page_title")

    full_title = f"{title}{separator}{site_name}" if title else site_name
    return mark_safe(f"<title>{full_title}</title>")
