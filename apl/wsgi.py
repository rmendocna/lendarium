"""
WSGI config for apl project.

It exposes the WSGI callable as a module-level variable named ``application``.

"""

import os
import sys

from django.core.wsgi import get_wsgi_application
sys.path.append('/home/bitnami/projects/lendarium')
os.environ.setdefault("PYTHON_EGG_CACHE", "/home/bitnami/projects/lendarium/egg_cache")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apl.settings')

application = get_wsgi_application()
