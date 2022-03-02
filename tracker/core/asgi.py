"""
ASGI config for tracker project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

from decouple import config

os.environ.setdefault(config("DJANGO_SETTINGS_MODULE", default="core.settings.local"))

application = get_asgi_application()
