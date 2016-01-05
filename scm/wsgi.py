"""
WSGI config for scm project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application


# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scm.settings")
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)
os.environ["DJANGO_SETTINGS_MODULE"]="scm.settings"

application = get_wsgi_application()
