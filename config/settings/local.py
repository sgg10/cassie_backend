"""Development settings."""

from .base import *
from .base import env

# Base
DEBUG = True

# Security
SECRET_KEY = env('DJANGO_SECRET_KEY', default='nc#4bjwisbtlketyx3ha4ezv%y=yp1yolb7g7n%df$1z_q!*p9')
ALLOWED_HOSTS = [
  'localhost',
  '0.0.0.0',
  '127.0.0.1',
]

# Cache
CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    'LOCATION': ''
  }
}

# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# django-extensions
INSTALLED_APPS += ['django_extensions']

# Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True