"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os, json

import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_ENV = os.environ.setdefault('ENVIRONMENT','local')
SECRET_KEY = os.environ.setdefault('SECRET_KEY', 'xxxx')

# Application Configuration 
PRODUCTION_URL="ccda.app.cloud.gov"

# Email Configuration
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST=os.getenv('EMAIL_HOST')
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER=os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=os.getenv('EMAIL_HOST_PASSWORD')

# Environment Specific Configuration
if APP_ENV == 'cloud':
    DEBUG = False
    aws_creds = json.loads(os.getenv('VCAP_SERVICES'))['s3'][0]['credentials']
    db_creds = json.loads(os.getenv('VCAP_SERVICES'))['aws-rds'][0]['credentials']
else:
    DEBUG = True
    aws_creds={
        'access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
        'secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'bucket': os.getenv('AWS_BUCKET_NAME'),
        'region': os.getenv('AWS_DEFAULT_REGION'),
    }
    db_creds={
        'host': os.getenv('POSTGRES_HOST'),
        'db_name': os.getenv('POSTGRES_DB'),
        'username': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'port': os.getenv('POSTGRES_PORT')
    }

# General Application Configuration
ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'drf_yasg',
    'rest_framework',
    'corsheaders',

    'uaa_client',

    'authentication.apps.AuthenticationConfig',
    'api.apps.ApiConfig',
    'files.apps.FilesConfig'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django_referrer_policy.middleware.ReferrerPolicyMiddleware',
    
    'django.middleware.security.SecurityMiddleware',
    
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    
    'core.middleware.DebugMiddleware',
    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'uaa_client.middleware.UaaRefreshMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Public REST Framework Configuration 
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# Database Configuration Settings
DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'HOST': db_creds['host'],
    'NAME': db_creds['db_name'],
    'USER': db_creds['username'],
    'PASSWORD': db_creds['password'],
    'PORT': db_creds['port']
    }
}

# Localization Configuration Settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# CSRF Settings
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_PATH = '/'

# Miscellanous Header Properties
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
REFERRER_POLICY = 'origin'

# cloud.gov OAuth2 properties
AUTHENTICATION_BACKENDS = [
    'uaa_client.authentication.UaaBackend'
]

LOGIN_URL = 'uaa_client:login'
LOGIN_REDIRECT_URL = '/success'
UAA_APPROVED_DOMAINS = ['gsa.gov']
UAA_CLIENT_ID = os.getenv('UAA_CLIENT_ID', 'fakeclientid')
UAA_CLIENT_SECRET = os.getenv('UAA_CLIENT_SECRET', 'fakeclientsecret')

if APP_ENV == 'cloud':
    UAA_LOGOUT_URL = 'https://login.fr.cloud.gov/logout.do'
    UAA_AUTH_URL = 'https://login.fr.cloud.gov/oauth/authorize'
    UAA_TOKEN_URL = 'https://uaa.fr.cloud.gov/oauth/token'
else:
    UAA_AUTH_URL = 'fake:'
    UAA_TOKEN_URL = 'fake:'

# Static Configuration
STATIC_URL = '/static/'
STATICFILES_DIR = [ ]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# S3 File Upload Configuration
ALLOWED_MIMETYPES=['application/pdf']

