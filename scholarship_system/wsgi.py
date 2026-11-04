"""
WSGI config for scholarship_system project.

It exposes the WSGI callable as a module-level variable named ``application``.
For Vercel deployment, it also exposes ``app``.
"""

import os
import sys
from pathlib import Path

# Add project root directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarship_system.settings')

application = get_wsgi_application()
app = application  # Required alias for Vercel

# Auto-migrate and seed demo data on Vercel if needed
if os.environ.get('VERCEL'):
    try:
        from django.core.management import call_command
        from django.db import connection
        tables = connection.introspection.table_names()
        if not tables or 'django_session' not in tables:
            call_command('migrate', interactive=False)
            from scholarships.models import Scholarship
            if Scholarship.objects.count() == 0:
                import setup_demo
    except Exception as e:
        print("Vercel startup notice:", e)
