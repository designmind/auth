from django.core.wsgi import get_wsgi_application
import os
import sys

# edit your username below
sys.path.append("/home/izmtky/public_html")


os.environ['DJANGO_SETTINGS_MODULE'] = 'auth.settings'

application = get_wsgi_application()
