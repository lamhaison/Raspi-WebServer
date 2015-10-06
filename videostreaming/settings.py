"""
Django settings for videostreaming project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cs=ou()e73i!lj#9n_na7g!2)$8=1vhzcwl8bv@r*n1m!jcpki'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'viewcam',
    'django_ajax',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)



ROOT_URLCONF = 'videostreaming.urls'


TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
# TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

WSGI_APPLICATION = 'videostreaming.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'webdb',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '123qwer',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Saigon'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/www/log/viewcam.log',
            'formatter': 'verbose'
        },

        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'viewcam': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
    }
}

'''
CACHES = {
'default': {
'BACKEND' : 'django.core.cache.backends.memcached.MemcachedCache',
'LOCATION' : '127.0.0.1:11211'
}
}
'''


SESSION_COOKIE_AGE = 1800

TIMER_NUMBER = 4
TIMER_LIST = [1, 2, 3, 4]
DEVICE_NUMBER = 4
DEV_LIST = [1, 2, 3, 4]
MAX_COUNT = 1

CONNECTION_URL = '127.0.01'
CONNECTION_PORT = '3306'
CONNECTION_USER = 'root'
CONNECTION_PASSWORD = '123qwer'
CONNECTION_DB_NAME = 'webdb'
VIDEO_DIR = '/var/www/video'
CONTROL_CAM_PATH = '/usr/share/control'
EXTENSION_VIDEO_FILE = 'h264'
# Unit is minute
INTERVAL_VIDEO = 60 * 3
# Unit is minute
INTERVAL_DAY_DELETE = (60 * 24 * 1)

# Alert for fire
FIRE_TEMPERATURE = 90

VIDEO_TYPE_OPTION = (
    ('bitrate', 'Bitrate'),
    ('fps', 'Frame per second'),
    ('size', 'Size'),
)










