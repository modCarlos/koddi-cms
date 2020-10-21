"""
Django settings for blog project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*r3qyvp6c$!7m8rw4j#my1okahmzv0a*1zn=db8!+u7&&(1%^l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

"""
    Config and Apps Section
"""

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_wysiwyg',
    'ckeditor',
    'endless_pagination',
    'page',
    #'south',
    'wp_admin',
    'eventon',
    #'tastypie',
    'payments',
    #'service',
    'rest_framework',
    #'snippets',
    'restservices'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'blog.urls'

WSGI_APPLICATION = 'blog.wsgi.application'


"""
    Database Section
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

"""
    Cache Section
"""
CACHES = {
   'default': {
       'BACKEND': 'redis_cache.RedisCache',
       'LOCATION': '127.0.0.1:6379',
       'OPTIONS': {
           'DB': 1
       },
   },
}

"""
    Time-Zone Section
"""

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

"""
    Static Files Section
"""

STATIC_PATH = os.path.join(PROJECT_PATH,'static/')

STATIC_URL = '/static/' # You may find this is already defined as such.

STATICFILES_DIRS = (
    STATIC_PATH,
)

"""
    Templates Section
"""

TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')

TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)

"""
    CKEditor Section - Editor of web pages for users
"""

DJANGO_WYSIWYG_FLAVOR = "ckeditor"
CKEDITOR_UPLOAD_PATH = "uploads/"

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

#Facebook connect
"""
    Facebook connect Section
"""
FACEBOOK_APP_ID = '958236160899463'
FACEBOOK_SECRET_KEY = '371bf8a27a104550b3351d58233c7c90'
#Warning! Modify only with the installer
#This is the secre key for encrypt the password at facebook connect
SECRET_FB_KEY = '306096903'

"""
    Email Section
"""
EMAIL_BACKEND = 'django.core.mail.backends,smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'carlos.osram@gmail.com'
EMAIL_HOST_PASSWORD = 'mi_password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

"""
    Payments Section
"""
PAYMENT_HOST = 'localhost:8080'
PAYMENT_USES_SSL = False
PAYMENT_MODEL = 'page.Payment'
PAYMENT_VARIANTS = {
    'default': ('payments.dummy.DummyProvider', {})}

"""
    Settings Section
"""
USE_CART = True
USE_NOTIFICATIONS = False