import os
import sys

# Add your project directory to the sys.path
path = '/home/amaan4/spotter-ai-assessment/backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'

# Setup Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
