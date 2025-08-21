from core.settings.conf import *  # noqa: F403

ROOT_URLCONF = "dashboard.settings.urls"

ALLOWED_HOSTS += [  # noqa: F405
    "dev.treeolive.tech",
    "bigpen.tawalabora.space",
    "bigpen.co.ke",
    "www.bigpen.co.ke",
    "preview.bigpen.co.ke",
]

INSTALLED_APPS += [  # noqa: F405
    "dashboard.orders",
    "dashboard.stock",
    "dashboard.seed",
]

# AUTH_USERNAME = {
#     "label": "Username",
#     "placeholder": "Enter your username",
# }

# EMAIL_HOST_USER = config("EMAIL_HOST_USER", default=None)
# EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default=None)
# EMAIL_HOST = config("EMAIL_HOST", default=None)
