# File: salonAppBackend/settings.py

import os
from pathlib import Path
from datetime import timedelta
from celery.schedules import crontab

# ──────────────────────────────────────────────────────────────────────────────
# BASE_DIR
# ──────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ──────────────────────────────────────────────────────────────────────────────
# SECRET KEY & DEBUG
# ──────────────────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG      = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# ──────────────────────────────────────────────────────────────────────────────
# INSTALLED APPS
# ──────────────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third‑party
    'django_filters',
    'rest_framework',
    'drf_spectacular',
    'corsheaders',
    'storages',
    'django_celery_beat',
    'django_celery_results',

    # Your apps
    'usersapp',
    'authapp',
    'followApp',
    'ai_features',
    'shopDashboardApp',
    'companyApp',
    'shopApp',
    'customersApp',
    'shopServiceApp',
    'reviewapp',
    'subscriptionApp',
    'payment.apps.PaymentConfig',
    'reelsApp',
    'storiesApp.apps.StoriesAppConfig',
    'employeeApp',
    'notificationsapp',
    'adsApp',
    'chatApp',
]

# ──────────────────────────────────────────────────────────────────────────────
# MIDDLEWARE
# ──────────────────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# ──────────────────────────────────────────────────────────────────────────────
# AUTH & URLS
# ──────────────────────────────────────────────────────────────────────────────
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'managers_auth_backend.ManagerPhoneBackend',
]
ROOT_URLCONF = 'salonAppBackend.urls'
ASGI_APPLICATION = "salonAppBackend.asgi.application"

# ──────────────────────────────────────────────────────────────────────────────
# TEMPLATES
# ──────────────────────────────────────────────────────────────────────────────
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

# ──────────────────────────────────────────────────────────────────────────────
# DATABASES
# ──────────────────────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ──────────────────────────────────────────────────────────────────────────────
# PASSWORD VALIDATORS
# ──────────────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ──────────────────────────────────────────────────────────────────────────────
# INTERNATIONALIZATION & STATIC / MEDIA
# ──────────────────────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True

STATIC_URL = 'static/'
MEDIA_URL  = f'https://{os.environ.get("AWS_S3_CUSTOM_DOMAIN","your-bucket.s3.your-region.amazonaws.com")}/media/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ──────────────────────────────────────────────────────────────────────────────
# REST FRAMEWORK + SPECTACULAR
# ──────────────────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE':       'QueueMe API',
    'DESCRIPTION': 'All endpoints for Queue Me backend services',
    'VERSION':     '1.0.0',
    # <-- ENUM_NAME_OVERRIDES has been removed entirely
}

# ──────────────────────────────────────────────────────────────────────────────
# SIMPLE JWT
# ──────────────────────────────────────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(minutes=144000),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS':  True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# ──────────────────────────────────────────────────────────────────────────────
# CORS
# ──────────────────────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = ["https://shop.queueme.net"]
CORS_ALLOW_METHODS   = ["DELETE","GET","OPTIONS","PATCH","POST","PUT"]

# ──────────────────────────────────────────────────────────────────────────────
# AWS S3 MEDIA
# ──────────────────────────────────────────────────────────────────────────────
AWS_ACCESS_KEY_ID     = os.environ.get('AWS_ACCESS_KEY_ID','')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY','')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME','')
AWS_S3_REGION_NAME    = os.environ.get('AWS_S3_REGION_NAME','')
AWS_S3_CUSTOM_DOMAIN  = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
AWS_DEFAULT_ACL       = 'public-read'
AWS_QUERYSTRING_AUTH  = False
DEFAULT_FILE_STORAGE  = 'storages.backends.s3boto3.S3Boto3Storage'

CSRF_TRUSTED_ORIGINS = [
    "https://api.queueme.net",
    "http://localhost:3000",
    "https://shop.queueme.net",
]

# ──────────────────────────────────────────────────────────────────────────────
# CHANNEL LAYERS
# ──────────────────────────────────────────────────────────────────────────────
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# ──────────────────────────────────────────────────────────────────────────────
# CELERY
# ──────────────────────────────────────────────────────────────────────────────
CELERY_BROKER_URL        = os.environ.get('CELERY_BROKER_URL','redis://localhost:6379/0')
CELERY_RESULT_BACKEND    = 'django-db'
CELERY_CACHE_BACKEND     = 'default'
CELERY_BEAT_SCHEDULER    = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_TIMEZONE          = TIME_ZONE
CELERY_BEAT_SCHEDULE     = {
    'daily-ai-forecast-update': {
        'task':    'shopServiceApp.tasks.recalc_all_forecasts',
        'schedule': crontab(hour=0, minute=0),
        'options': {'queue': 'forecasting'},
    },
    'process-recurring-payments': {
        'task':    'subscriptionApp.tasks.process_recurring_payments',
        'schedule': 60.0,
    },
}
