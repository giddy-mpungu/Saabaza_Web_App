from .base import *  # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'appsaabaza_edms',
        'USER': 'root',
        'HOST': 'mysql',
        'PORT': '3306',
    }
}
