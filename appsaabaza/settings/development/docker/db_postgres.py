from .base import *  # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PASSWORD': 'appsaabazauserpass',
        'PORT': '5432',
    }
}
