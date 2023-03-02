"""
WSGI config for TailorApp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from threading import Thread

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TailorApp.settings')

application = get_wsgi_application()

# start create reminder thread after runserver command is called.
from tailor_api.views import create_reminders
t = Thread(target=create_reminders)
t.start()

