#---pip install psycopg2-binary django-environ


import environ
import os

# Инициализация environ
env = environ.Env()
environ.Env.read_env()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hackathon',
        'USER': 'postgres',
        'PASSWORD': '11062004',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}