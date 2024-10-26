from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':  'libros',
        'USER': 'postgres',
        'PASSWORD': 'koala',
        'HOST': '127.0.0.1',
        'DATABASE_PORT': '5432'
    }
}