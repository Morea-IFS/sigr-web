from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY",)
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

HOST = os.getenv("HOST", "*")
ALLOWED_HOSTS = [h.strip() for h in HOST.split(",")] if HOST else ["*"]

INSTALLED_APPS = [
    'daphne',
    'channels',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'pwa',
    'app',
    'dress',
    'detonador',
    'remote',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sigr.urls'
WSGI_APPLICATION = 'sigr.wsgi.application'
ASGI_APPLICATION = 'sigr.asgi.application'

REDIS_SECRET_KEY = os.getenv("REDIS_SECRET_KEY", "default_redis_key")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'app' / 'templates',
            BASE_DIR / 'dress' / 'templates',
            BASE_DIR / 'detonador' / 'templates',
        ],
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

DBTYPE = os.getenv("DBTYPE", "SQLite3").lower()

if DBTYPE == "mysql":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv("DBNAME"),
            'USER': os.getenv("DBUSER"),
            'PASSWORD': os.getenv("DBPASSWORD"),
            'HOST': os.getenv("DBHOST", "localhost"),
            'PORT': os.getenv("DBPORT", "3306"),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_USER_MODEL = 'app.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True   
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV").upper()

if ENVIRONMENT == "PROD":
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/')]
    MEDIA_ROOT = '/var/www/html/SIGR/media/'
    STATIC_ROOT = '/var/www/html/SIGR/static/'
else:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/')]
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    "site_title": "Painel Admin",
    "site_header": "SIGR",
    "site_brand": "SIGR ADMIN",
    "site_logo": "images/morea.png",
    "show_sidebar": True,
    "navigation_expanded": False,
    "hide_apps": [],
    "hide_models": [],
    "topmenu_links": [
        {"name": "Site Principal", "url": "/"},
        {"model": "auth.User"},
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "app": "fas fa-cogs",
        "dress": "fas fa-tshirt",
        "detonador": "fas fa-bolt",
        "remote": "fas fa-tv-alt", 
        "dress.Dress": "fas fa-lightbulb",
        "dress.Device": "fas fa-microchip",
        "remote.Remote": "fas fa-gamepad",
        "detonador.Evento": "fas fa-calendar-alt",
        "detonador.Device": "fas fa-cpu",
    },
    "changeform_format": "horizontal_tabs",
    "order_with_respect_to": ["dress", "detonador", "remote", "app"],
}

PWA_APP_NAME = 'SIGR App'
PWA_APP_DESCRIPTION = "Sistema Integrado SIGR"
PWA_APP_THEME_COLOR = "#21B0E9"
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/images/icon-160x160.png',
        'sizes': '160x160'
    },
    {
        'src': '/static/images/icon-512x512.png',
        'sizes': '512x512'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/images/icon-160x160.png',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/icon-512x512.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'pt-BR'
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static', 'js', 'serviceworker.js')