#conding=utf-8
"""
Django settings for DaibeiServer project.

Generated by 'django-admin startproject' using Django 1.8.16.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qg0^jeww36dp$d-&lbm0j*%!ik4^7(qfps0ll12o_(zdd@)srr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['119.23.45.38']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
    'resourceManager',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'DaibeiServer.urls'

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

WSGI_APPLICATION = 'DaibeiServer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Caches
CACHES = {
    'default' : {
        'BACKEND' : 'django_redis.cache.RedisCache',
        'LOCATION' : 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS':'django_redis.client.DefaultClient',
        },
    },
}

# LOG 
LOGGING = {
    'version' : 1,                  
    'disable_existing_loggers' : True,  
    
    'formatters' : {                    
        
        'verbose' : {                   
            'format' : '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple' : {                    
            'format' : '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    
    'filters' : {                       
        'special' : {                   
     
            'require_debug_true' : {
                '()' : 'django.utils.log.RequireDebugTrue',
                'foo' : 'bar',
            },
        },                 
    },
    
    'handlers' : {                          
    
        'null' : {                      
            'level' : 'DEBUG',
            'class' : 'logging.NullHandler'
        },

        'console' : {                   
            'level' : 'DEBUG',
            'class' : 'logging.StreamHandler',
        },

        'default' : {
            'level' : 'DEBUG',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : '/root/log/DaibeiDebug.log',
            'formatter' : 'verbose',
        },

        'mail_admins' : {                   
                                            
            'level' : 'ERROR',
            'class' : 'django.utils.log.AdminEmailHandler',
            'filters' : ['special']
        }
    },

    'loggers' : {                   
        'django' : {                        
            'handlers' : ['null'],
            'propagate' : 'True',
            'level' : 'INFO',
        },
        
        'django.request' : {        
            'handlers' : ['mail_admins'],
            'level' : 'ERROR',
            'propagate' : 'False',
        },

        'DaibeiServer.custom' : {  
            'handlers' : ['default','console','mail_admins'],
            'level' : 'INFO',
            'filters' : ['special'],
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')



