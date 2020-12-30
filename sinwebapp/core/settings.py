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

# Localization Configuration
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Application Configuration 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_ENV = os.environ.setdefault('APP_ENV','local')
SECRET_KEY = os.environ.setdefault('SECRET_KEY', 'xxxxxxxxxx')

meta_file = os.path.join(BASE_DIR, 'metadata.json')
with open(meta_file) as f:
    metadata = json.load(f)

PRODUCTION_URL=metadata['production_url']
VERSION=metadata['version']
MAINTAINER=metadata['maintainer']

# Development Mode Configuration
DEVELOPMENT_MODE=os.environ.setdefault('DEVELOPMENT', 'False')
DEV_EMAIL="chinchalinchin@gmail.com"
DEV_GROUP="admin_group"

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
elif APP_ENV == 'mcaas':
    # TODO
    
    pass
elif APP_ENV == 'local' or APP_ENV == 'container':
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

# Database Configuration Settings
if APP_ENV == 'local' or APP_ENV == 'container' or APP_ENV == 'cloud':
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
elif APP_ENV == 'mcaas':
    # TODO:

    pass

# General Application Configuration
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

# Django Module Configuration
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
    'authentication.apps.AuthenticationConfig',
    'api.apps.ApiConfig',
    'files.apps.FilesConfig'
]
if APP_ENV == 'local' or APP_ENV == 'container' or APP_ENV == 'cloud':
    INSTALLED_APPS += ['uaa_client']
elif APP_ENV == 'mcaas':
    # TODO

    pass

# Middleware Order Configuration
if APP_ENV == 'local' or APP_ENV == 'container' or APP_ENV == 'cloud':
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
elif APP_ENV == 'mcaas':
    # TODO
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
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    pass

# Template Configuration
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
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# CSRF Configuration
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_PATH = '/'

# CORS Configuration
# CORS_ALLOWED_ORIGINS = ['http://localhost:4200', 'http://localhost:8000', 
  #                      'http://localhost', f'https://{PRODUCTION_URL}']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Miscellanous Headers Configuration
REFERRER_POLICY = 'origin'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', PRODUCTION_URL]

# Authentication Configuration
if APP_ENV == 'local' or APP_ENV == 'container' or APP_ENV == 'cloud':
    AUTHENTICATION_BACKENDS = [ 'uaa_client.authentication.UaaBackend' ]
    LOGIN_URL = 'uaa_client:login'
    LOGIN_REDIRECT_URL = '/success'
    UAA_APPROVED_DOMAINS = ['gsa.gov']
    UAA_CLIENT_ID = os.getenv('UAA_CLIENT_ID', 'fakeclientid')
    UAA_CLIENT_SECRET = os.getenv('UAA_CLIENT_SECRET', 'fakeclientsecret')

    if APP_ENV == 'cloud':
        UAA_LOGOUT_URL = 'https://login.fr.cloud.gov/logout.do'
        UAA_AUTH_URL = 'https://login.fr.cloud.gov/oauth/authorize'
        UAA_TOKEN_URL = 'https://uaa.fr.cloud.gov/oauth/token'

    elif APP_ENV == 'local' or APP_ENV == 'container':
        UAA_AUTH_URL = 'fake:'
        UAA_TOKEN_URL = 'fake:'

elif APP_ENV == 'mcaas':
    AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

    
    pass
 

# Static Configuration
STATIC_URL = '/static/'
STATICFILES_DIR = [ ]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# S3 File Upload Configuration
ALLOWED_MIMETYPES=['application/pdf']

