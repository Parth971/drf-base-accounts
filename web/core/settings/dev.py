import os

from core.settings.base import *
from datetime import timedelta

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'PORT': os.environ.get('DB_PORT'),
        'HOST': os.environ.get('DB_HOST')
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=int(os.environ.get('ACCESS_TOKEN_LIFETIME'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(seconds=int(os.environ.get('REFRESH_TOKEN_LIFETIME'))),
}

FRONT_END_DOMAIN = os.environ.get('FRONT_END_DOMAIN')

# Forgot password link expiry time
PASSWORD_RESET_TIMEOUT = int(os.environ.get("PASSWORD_RESET_TIMEOUT"))

MEDIA_ROOT = BASE_DIR / 'media_files'
MEDIA_URL = '/media/'

