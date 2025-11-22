"""
Django settings for Saboreie project.
"""

from pathlib import Path
import os

# -------------------------------------------------
# BASE_DIR
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------------------------------------
# SEGURANÇA
# -------------------------------------------------
SECRET_KEY = 'django-insecure-5*t@y9hf#3kjf1lz4#@!yi@4$qftf1#t3-5!otqbhf)df#u=ni'

DEBUG = False   # Render = produção

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "saborize-3.onrender.com",
]


# -------------------------------------------------
# APPS
# -------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'autenticacao.apps.AutenticacaoConfig',
    'django_bootstrap5',
    'receitas.apps.ReceitasConfig',
]

AUTH_USER_MODEL = 'autenticacao.User'


# -------------------------------------------------
# MIDDLEWARE + WHITENOISE
# -------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise para servir arquivos estáticos no Render
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# -------------------------------------------------
# URLS / TEMPLATES / WSGI
# -------------------------------------------------
ROOT_URLCONF = 'Saboreie.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Saboreie.wsgi.application'


# -------------------------------------------------
# DATABASE
# -------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# -------------------------------------------------
# VALIDAÇÃO DE SENHA
# -------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# -------------------------------------------------
# LOCALIZAÇÃO
# -------------------------------------------------
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# -------------------------------------------------
# STATIC FILES (Render + WhiteNoise)
# -------------------------------------------------
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise: gera versões comprimidas
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# -------------------------------------------------
# MEDIA FILES (uploads do usuário)
# -------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# -------------------------------------------------
# CONFIG LOGIN
# -------------------------------------------------
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# -------------------------------------------------
# AVOID CRASHES ON COLLECTSTATIC (Render)
# -------------------------------------------------
if os.environ.get("RENDER"):
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
