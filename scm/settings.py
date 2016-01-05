"""
Django settings for scm project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from datetime import timedelta
import djcelery
djcelery.setup_loader()
CELERY_TIMEZONE="Asia/Shanghai"
BROKER_URL = 'redis://127.0.0.1:6379/11'
CELERYBEAT_SCHEDULE = {
    'every-seconds-1': {
        'task': 'tasks.add',
        'schedule': timedelta(seconds=3),
        'args':(3,5)
    },
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '959pnv02y=9dyry1k0mypr8&m)a^pv7-x7cx3rtogleb4w*ty5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'base',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
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


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
   'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kgscm',
        'USER': 'root',
        'PASSWORD': '10233201sn',
        'HOST': '192.168.122.146',
        'PORT': '3306',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        },
    },
}
REDIS_TIMEOUT=7*24*60*60
CUBES_REDIS_TIMEOUT=60*60
NEVER_REDIS_TIMEOUT=365*24*60*60

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
#上传文件
MEDIA_URL = '/upload/'
MEDIA_ROOT = 'upload'

# ***配置：静态文件（CSS、JS）路径***
STATIC_URL = '/static/'
STATIC_ROOT="comm_static"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,  'static'),
)

LOGIN_URL ="/scm/base/loginpage"
LOGIN_EXEMPT_URLS=["scm/base/login","scm/base/logout","scm/base/vcode/","favicon.ico"]


#linux配置static
# STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, "static"),
#    '/var/www/scm/static',
# ]
# STATIC_ROOT = os.path.join(BASE_DIR, "scm_static/")

# ***自定义日志输出信息***
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
