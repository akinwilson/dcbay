import os 
from pathlib import Path
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG =  True if os.getenv("DEBUG") == "True" else False

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",  # install session db
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "store",
    "basket",
    "account",
    "orders",
    "payment",
    "extract",
    "review",
    "django_extensions",
]

MIDDLEWARE = [
    "django.middleware.csrf.CsrfViewMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",  # for sessions to work needed
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# SSL settings
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True 
# CSRF_COOKIE_SECURE = True



ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",") # ["*"] # 

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
] if DEBUG else os.getenv('TRUSTED_ORIGINS').split(",")

CSRF_HEADER_NAME = "HTTP_X_CSRFTOKEN"


ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "store.context_processors.categories",
                "basket.context_processors.basket",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": "localTestingDeleteMe",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"), # "postgresDB",
        "USER": os.getenv("POSTGRES_USER"), # "postgresUser",
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"), #  "postgresPW",
        "HOST":  os.getenv("POSTGRES_HOST"), #"postgres",  #  "127.0.0.0",  # "postgres"
        "PORT":  os.getenv("POSTGRES_PORT"), #"5432",  # "5455",
    },
    "crypto": {
        "NAME": os.getenv("BITCOIN_DB"), # "bitcoinlib",
        "USER": os.getenv("BITCOIN_USER"), #"bitcoinlib",
        "PASSWORD": os.getenv("BITCOIN_PASSWORD"), #"password",
        "HOST": os.getenv("BITCOIN_HOST"), #"postgres",  #  "127.0.0.0",
        "PORT": os.getenv("BITCOIN_PORT"), #"5432",  # "5455",  #
    },
}



AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

if not DEBUG:
    STATIC_ROOT =  "/static/"
    MEDIA_ROOT =  "/media/"

STATIC_URL = "/static/"
MEDIA_URL = "/media/"


STATICFILES_DIRS = [BASE_DIR / "static", BASE_DIR / "media"]

#### FOR LOCAL DEBUGGING SWITCH THIS BACK ON
if DEBUG:
# Two settings, working locally with media folder
    # set STATIC_ROOT for development to no location
    STATIC_ROOT = "" #/ BASE_DIR / "static"
    MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Basket session ID
BASKET_SESSION_ID = "basket"

# Bitcoin settings
SERVER_WALLET_NAME = os.getenv("SERVER_WALLET_NAME")
PRIVATE_MNEMONIC = os.getenv("PRIVATE_MNEMONIC") 
SHIPPING_COST = os.getenv("PAYMENT_SHIPPING_COST") # "0.10"
# payment configs 
PAYMENT_NETWORK = os.getenv("PAYMENT_NETWORK")
PAYMENT_PRECENTAGE_LEEWAY = os.getenv("PAYMENT_PRECENTAGE_LEEWAY")
PAYMENT_OFFLINE = os.getenv("PAYMENT_OFFLINE")

# Custom user model
AUTH_USER_MODEL = "account.UserBase"
LOGIN_REDIRECT_URL = "/account/dashboard"
LOGIN_URL = "/account/login/"

# Email setting
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "neuro.testing123@gmail.com"
EMAIL_HOST_PASSWORD = "password"


# cache setup to use redis
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379",
    }
}

# Celery settings
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_TASK_ALWAYS_EAGER  = True if DEBUG else False 
CELERY_BEAT_SCHEDULE = {
    "payment_confirmation_task": {
        "task": "payment.tasks.payment_confirmations",
        "schedule": crontab(minute="*/1") if DEBUG else crontab(hour="*/1"),
    },
    "daily_shipments_task": {
        "task": "payment.tasks.daily_shipments",
        "schedule": crontab(minute="*/1") if DEBUG else crontab(hour="*/24"),
    },
    "daily_exchange_rate": {
        "task": "payment.tasks.daily_bitcoin_exchange_rate",
        "schedule": crontab(minute="*/1") if DEBUG else crontab(hour="*/12")
    }
}


LOGGING = {
    "version": 1,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "bitcoinlib":{
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

if DEBUG:
    # make all loggers use the console.
    for logger in LOGGING["loggers"]:
        LOGGING["loggers"][logger]["handlers"] = ["console"]
