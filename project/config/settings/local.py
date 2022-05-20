from .base import *

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

BROWSER_DRIVER_PATH = config("BROWSER_DRIVER_PATH", default="None")

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
