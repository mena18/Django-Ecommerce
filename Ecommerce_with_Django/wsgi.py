import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce_with_Django.settings')

application = get_wsgi_application()
