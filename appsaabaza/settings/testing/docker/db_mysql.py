from .base import *  # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'appsaabaza',
        'USER': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}