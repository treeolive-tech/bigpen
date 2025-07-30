from core.settings.conf import *  # noqa: F403

ROOT_URLCONF = "custom.settings.urls"

ALLOWED_HOSTS += [  # noqa: F405
    "dev.tawalabora.space",
    "bigpen.co.ke",
    "www.bigpen.co.ke",
    "preview.bigpen.co.ke",
]

INSTALLED_APPS += [  # noqa: F405
    "custom.orders",
    "custom.stock",
    "custom.seed",
]

FRONTEND_WEB_URL = "https://www.bigpen.co.ke"

# AUTH_USERNAME = {
#     "label": "Username",
#     "placeholder": "Enter your username",
# }
