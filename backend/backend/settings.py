"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from socket import gethostname, gethostbyname

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nin4lv1^q#kj3mrd(v6a#d7apuo7(6w$k56cc8@8#ptf90drz*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG", True))

ALLOWED_HOSTS = [ gethostname(), gethostbyname(gethostname()), '34.95.29.94', 'localhost', '127.0.0.1'] 

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend.main',
    'webpack_loader',
    'django_crontab',
    'corsheaders',
]

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

ROOT_URLCONF = 'backend.urls'
 
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'main-db',
        'HOST': os.environ.get("MONGO_DB_ADDR", "localhost"),
        'PORT': os.environ.get("MONGO_DB_PORT", 27017),
        'ENFORCE_SCHEMA': False,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# twitter api access information
# https://python-twitter.readthedocs.io/en/latest/getting_started.html

TWITTER_API_ACCESS = {
    'TWT_API_KEY': '7qmxgNzLQZOYEqFLV5VbViT2q',
    'TWT_API_SECRET': 'S2OlKXHwAO9Kuf4AOYYNF1hiQVSP1g0hwV0GRs8OpTEitrW01W',
    'TWT_ACCESS_TOKEN': '2931606853-deuoJF5HiN3hCPPfV4wRnBNqN77by0oYBrYzXLm',
    'TWT_ACCESS_SECRET': '5o6kpYwNJXMKkN2GuQBUuaXJQpJhMjjlgi8Jq1YmDONKZ'
}

CORS_ORIGIN_ALLOW_ALL = True

# subscription jobs
CRONJOBS = [
    ('*/1 * * * *', 'backend.subcription_job', '>> /tmp/tweets.log')
]