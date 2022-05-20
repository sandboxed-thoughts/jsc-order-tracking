import os

from django.core.asgi import get_asgi_application

from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", config("DJANGO_SETTINGS_MODULE", default="config.settings.local"))

application = get_asgi_application()
