"""Base settings to build other settings files upon."""

import environ
from datetime import timedelta
from pathlib import Path

ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('cassie')

env = environ.Env()

# Base
DEBUG = env.bool('DJANGO_DEBUG', False)

# Language and timezone
TIME_ZONE = 'America/Bogota'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_I10N = True
USE_TZ = True

# DATABASE
DATABASES = {
  'default': env.db('DATABASE_URL'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# URLs
ROOT_URLCONF = 'config.urls'

# WSGI
WSGI_APPLICATION = 'config.wsgi.application'

# User & Authentication
AUTH_USER_MODEL = 'users.User'

# Apps
DJANGO_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
  'rest_framework',
  'django_filters',
  'corsheaders'
]

LOCAL_APPS = [
  'cassie.users.apps.UsersAppConfig',
  'cassie.licenses.apps.LicensesAppConfig',
  'cassie.accounts.apps.AccountsAppConfig',
  'cassie.reports.apps.ReportsAppConfig',
  'cassie.trades.apps.TradesAppConfig'
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Passwords
PASSWORD_HASHERS = [
  'django.contrib.auth.hashers.Argon2PasswordHasher',
  'django.contrib.auth.hashers.PBKDF2PasswordHasher',
  'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
  'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
  'django.contrib.auth.hashers.BCryptPasswordHasher',
]
AUTH_PASSWORD_VALIDATORS = [
  {
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  },
]

# Middlewares
MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'corsheaders.middleware.CorsMiddleware',
]

# Static files
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
STATIC_URL = '/static/'
STATIC_DIRS = [
  str(APPS_DIR.path('static'))
]
STATICFILES_FINDERS = [
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media
MEDIA_ROOT = str(APPS_DIR('media'))
MEDIA_URL = '/media/'

# Templates
TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
      str(APPS_DIR.path('templates')),
    ],
    'OPTIONS': {
      'debug': DEBUG,
      'loaders': [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
      ],
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.template.context_processors.i18n',
        'django.template.context_processors.media',
        'django.template.context_processors.static',
        'django.template.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]

# Security
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKED', default='django.core.mail.backends.smtp.EmailBackend')

# Admin
ADMIN_URL = 'admin/'
ADMINS = [
  """Santiago Elias Rodriguez Hawasly""", 'serodriguh@eafit.edu.co',
  """Julianny Restrepo Lopez""", 'jrestrepol@eafit.edu.co',
  """Rony Rafael Romero Mejia""", 'rrromerom@eafit.edu.co',
  """Sebastian Granda Gallego""", 'sgrandag@eafit.edu.co'
]
MANAGERS = ADMINS

# Celery
INSTALLED_APPS += ['cassie.taskapp.celery.CeleryAppConfig']
if USE_TZ:
  CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_TASK_TIME_LIMIT = 5 * 60
CELERYD_TASK_SOFT_TIME_LIMIT = 60

# Django REST Framework
REST_FRAMEWORK = {
  'DEFAULT_RENDERER_CLASSES': (
    'rest_framework.renderers.JSONRenderer',
  ),
  'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework_simplejwt.authentication.JWTAuthentication',
  ),
  'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

SIMPLE_JWT = {
  'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
  'ROTATE_REFRESH_TOKENS': True
}

# CORS
CORS_ORIGIN_ALLOW_ALL = True