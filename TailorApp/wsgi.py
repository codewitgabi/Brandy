"""
WSGI config for TailorApp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from threading import Thread
from tailor_api.views import create_reminders

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TailorApp.settings')

application = get_wsgi_application()

# start create reminder thread after runserver command is called.
t = Thread(target=create_reminders)
t.start()

