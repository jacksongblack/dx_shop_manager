# coding=utf-8

"""
Django settings for dx_bdos project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, \
    CACHES_LOCATION, CACHES_DB, CACHES_PASSWORD, LOG_PATH, DB_ENGINE

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ibp9x!nsdujx%krt(&c&+opms$$yy$h79hkgcqpmr7=7t6m69j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'users',
    # 'captcha',
    'django_cron',
    'south',
    'products',
    'categories',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dx_shop_manager.urls'

WSGI_APPLICATION = 'dx_shop_manager.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
#多数据源配置
DATABASE_ROUTERS = ['dx_shop_manager.router.DBRouter']

DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DB_NAME,  # Or path to database file if using sqlite3.
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': DB_PORT,  # Set to empty string for default.
    },
    #     'db1': {
    #         'ENGINE': DB_ENGINE, # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    #         'NAME': DB_NAME,                      # Or path to database file if using sqlite3.
    #         'USER': DB_USER,
    #         'PASSWORD': DB_PASSWORD,
    #         'HOST': DB_HOST,                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
    #         'PORT': DB_PORT,                      # Set to empty string for default.
    #     },
}
#定时器配置
CRON_CLASSES = [
    "django_cron.cron.TestCronJob",
]
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DEFAULT_CHARSET = 'utf-8'

#自定义user模板
AUTH_USER_MODEL = "users.User"

#自定义验证模块
AUTHENTICATION_BACKENDS = (
    'core.backends.CheckModelBackend',
)
#每个页面应该被缓存的秒数
CACHE_MIDDLEWARE_SECONDS = 15 * 60
CACHE_MIDDLEWARE_KEY_PREFIX = 'xinranzhijia'

STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static/')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    ('css', os.path.join(STATIC_ROOT, 'css').replace('\\', '/') ),
    ('js', os.path.join(STATIC_ROOT, 'js').replace('\\', '/') ),
    ('images', os.path.join(STATIC_ROOT, 'images').replace('\\', '/') ),
    ('font', os.path.join(STATIC_ROOT, 'font').replace('\\', '/') ),
    ('UE', os.path.join(STATIC_ROOT, 'UE').replace('\\', '/') ),
)

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../media/')
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), '../templates'),
)
UPLOAD_ROOT = os.path.join(os.path.dirname(__file__), "..")

#缓存设置使用Redis作为缓存服务器
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': CACHES_LOCATION,
        'OPTIONS': {
            'DB': CACHES_DB,
            'PASSWORD': CACHES_PASSWORD,
        },
    },
}

PAGINATE_BY = 10

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'core.authentication.MTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'page_size',
}
#日子配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'user_file_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH + 'bgos_user_log.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 500,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'user.logger': {
            'handlers': ['console', 'user_file_handler'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
IMAGE_MARK_FILE = BASE_DIR + "/media/image/logo.png"
IMAGE_ROOT_PATH = "/upload/images"
IMAGE_SIZE = {
    "60x60": {
        "width": "60",
        "height": "60"
    },
    "100x100": {
        "width": "100",
        "height": "100"
    }
}
# SOUTH_MIGRATION_MODULES = {
#     'captcha': 'captcha.south_migrations',
# }
