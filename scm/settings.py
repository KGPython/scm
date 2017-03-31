"""
Django settings for scm project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#-*- coding:utf-8 -*-
import os
from datetime import timedelta
from celery.schedules import crontab
import djcelery
from base.utils import Constants
djcelery.setup_loader()
CELERY_TIMEZONE="Asia/Shanghai"
BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERYBEAT_SCHEDULE = {
    'every-day-1': {
        'task': 'tasks.updateUser',
        'schedule': crontab(hour=13,minute=59), #crontab(hour=0,minute=1)
    },
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '959pnv02y=9dyry1k0mypr8&m)a^pv7-x7cx3rtogleb4w*ty5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False
# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['218.11.132.35','127.0.0.1','localhost','.ikuanguang.com']


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'djcelery',
    'base.timer',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'base.common.middlewares.LoginMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'scm.urls'
#CommonMiddleware相关
USE_ETAG=True
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'base.views.global_setting',

            ],
        },
    },
]

WSGI_APPLICATION = 'scm.wsgi.application'

#set session expire
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE=60*30  #30 minute


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': Constants.SCM_DB_MYSQL_DATABASE,
        'USER': Constants.SCM_DB_MYSQL_USER,
        'PASSWORD': Constants.SCM_DB_MYSQL_PASSWORD,
        'HOST': '192.168.250.18',
        'PORT': '3306',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': [
            '127.0.0.1:6379',
        ],

        "OPTIONS": {
            'DB':1,
            "PASSWORD":"kgredis",
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        },
        "KEY_PREFIX":'scm',
        # "TIMEOUT":480,

    },
    'redis2': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': [
            '127.0.0.1:6380',
        ],

        "OPTIONS": {
            'DB':2,
            "PASSWORD":"kgredis",
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        },
        "KEY_PREFIX":'scm',
    },
}
# REDIS_TIMEOUT=7*24*60*60
# CUBES_REDIS_TIMEOUT=60*60
# NEVER_REDIS_TIMEOUT=365*24*60*60

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True
#解决django日期与数据库日期差问题
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
#上传文件,scm.conf需要相应配置
MEDIA_URL = '/upload/'
MEDIA_ROOT = os.path.join(BASE_DIR,  'upload')

STATIC_URL = '/static/'
STATIC_ROOT="comm_static"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    #'/home/system/djangoapps/scm/static',
]

LOGIN_URL ="/scm/base/loginpage/"
LOGIN_EXEMPT_URLS=["scm/base/login/","scm/base/logout/","scm/base/vcode/","favicon.ico","scm/welcome"]

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'standard': {
#             'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
#     },
#     'filters': {
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'include_html': True,
#             },
#         'default': {
#             'level':'DEBUG',
#             'class':'logging.handlers.RotatingFileHandler',
#             'filename': 'log/all.log',
#             'maxBytes': 1024*1024*5,
#             'backupCount': 5,
#             'formatter':'standard',
#         },
#         'error': {
#             'level':'ERROR',
#             'class':'logging.handlers.RotatingFileHandler',
#             'filename': 'log/error.log',
#             'maxBytes':1024*1024*5,
#             'backupCount': 5,
#             'formatter':'standard',
#             },
#         'console':{
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'standard'
#         },
#         'request_handler': {
#             'level':'DEBUG',
#             'class':'logging.handlers.RotatingFileHandler',
#             'filename': 'log/script.log',
#             'maxBytes': 1024*1024*5,
#             'backupCount': 5,
#             'formatter':'standard',
#             },
#         'scprits_handler': {
#             'level':'DEBUG',
#             'class':'logging.handlers.RotatingFileHandler',
#             'filename':'log/script.log',
#             'maxBytes': 1024*1024*5,
#             'backupCount': 5,
#             'formatter':'standard',
#             }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['default', 'console'],
#             'level': 'DEBUG',
#             'propagate': False
#         },
#         'django.request': {
#             'handlers': ['request_handler'],
#             'level': 'DEBUG',
#             'propagate': False,
#             },
#         'scripts': {
#             'handlers': ['scprits_handler'],
#             'level': 'INFO',
#             'propagate': False
#         },
#         'blog.views': {
#             'handlers': ['default', 'error'],
#             'level': 'DEBUG',
#             'propagate': True
#         },
#     }
# }
