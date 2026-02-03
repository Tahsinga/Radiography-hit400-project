"""
ASGI config for MIC Radiology Management System
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mic_radiology.settings')
application = get_asgi_application()
