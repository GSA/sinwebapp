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

APP_ENV = os.getenv('ENVIRONMENT')

if APP_ENV == 'cloud' or APP_ENV == 'container':
    db_creds = json.loads(os.getenv('VCAP_SERVICES'))['aws-rds'][0]['credentials']
else:
    # app is being run locally 
    db_creds={
        'host': 'localhost',
        'db_name': 'sinwebapp',
        'username': 'postgres',
        'password': 'root',
        'port': '5432'
    }

SECRET_KEY = 'thisismyriflethisismygun'

if APP_ENV == "cloud":
    DEBUG = True
else: 
    DEBUG = True
    WEB_CONCURRENCY = 3

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'authentication.apps.AuthenticationConfig',
    'uaa_client',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'core.middleware.DebugMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'uaa_client.middleware.UaaRefreshMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

ALLOWED_HOSTS = ['*']

# Database Configuration

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

# Localization Configuration
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# cloud.gov OAuth2 properties
AUTHENTICATION_BACKENDS = [
    'uaa_client.authentication.UaaBackend'
]

LOGIN_URL = 'uaa_client:login'

LOGIN_REDIRECT_URL = '/success'

if APP_ENV == 'cloud':
    UAA_LOGOUT_URL = 'https://login.fr.cloud.gov/logout.do'
    UAA_AUTH_URL = 'https://login.fr.cloud.gov/oauth/authorize'
    UAA_TOKEN_URL = 'https://uaa.fr.cloud.gov/oauth/token'
    UAA_CLIENT_ID = os.getenv('UAA_CLIENT_ID')
    UAA_CLIENT_SECRET = os.getenv('UAA_CLIENT_SECRET')
else:
    UAA_AUTH_URL = 'fake:'
    UAA_TOKEN_URL = 'fake:'
    UAA_CLIENT_ID = 'fakeclientid'
    UAA_CLIENT_SECRET = 'fake-uaa-provider-client-secret'

UAA_APPROVED_DOMAINS = ['gsa.gov']

# Static Configuration
STATIC_URL = '/static/'

STATICFILES_DIR = [
    os.path.join(BASE_DIR, "static")
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
