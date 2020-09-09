from .base import *  # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'appsaabaza_edms',
        'USER': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
