"""
Django settings for tours_travels project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
from decouple import config

from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent 
# Import all constants to use throughout our application
try:
    from ecommerce.constants import *
except ImportError:
    pass



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "seen"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'pyuploadcare.dj',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'adminside',
    'users',
    'blog',
    'dede',
    'taggit',
    'crispy_forms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tours_travels.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'tours_travels.wsgi.application'

# Database
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
    

# }

# To use Neon with Django, you have to create a Project on Neon and specify the project connection settings in your settings.py in the same way as for standalone Postgres.

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'dedetraveln',
    'USER': 'dedetraveln_owner',
    'PASSWORD': 'npg_Ma7RYsHgW9Dy',
    'HOST': 'ep-late-boat-a5k7e5pp-pooler.us-east-2.aws.neon.tech',
    'PORT': '5432',
  }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
     
    
#     }
# }


# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)
X_FRAME_OPTIONS = 'SAMEORIGIN'
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

SITE_ID = 1
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

CRISPY_TEMPLATE_PACK='bootstrap4'

LOGIN_REDIRECT_URL='users:users-home'
LOGIN_URL='login'
LOGOUT_REDIRECT_URL = 'users:users-home'


## For media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media/')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

UPLOADCARE = {
  # Don’t forget to set real keys when it gets real :)

  'pub_key': 'f914008525312051b54c',
  'secret': '06f605e3fa31437f2a51',
}

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
    # Add to this list all the locations containing your static files 
)


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Or your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# Use app password for security
DEFAULT_FROM_EMAIL = 'novustellke@gmail.co'
EMAIL_HOST_USER='your_email@gmail.com'
EMAIL_HOST_PASSWORD='your_app_password'