"""
WSGI config for MIC Radiology Management System
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mic_radiology.settings')
application = get_wsgi_application()
