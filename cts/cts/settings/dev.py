from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '73e79fbd.ngrok.io']

EMAIL_SSL_KEYFILE = '/home/ave/PycharmProjects/cts/privkey.pem'
EMAIL_SSL_CERTFILE = '/home/ave/PycharmProjects/cts/fullchain.pem'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gisdb',
        'USER': 'geodjango',
        'PASSWORD': os.environ['DJANGO_DB_PASS'],
        'HOST': 'localhost',
        'PORT': '',
    }
}

try:
    from .local import *
except ImportError:
    pass
