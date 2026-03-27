from pathlib import Path
import os
import dj_database_url # type: ignore
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "True").lower() in ("1", "true", "yes", "on")
ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "*").split(",") if host.strip()]

# ================================
# EMAIL (SENDGRID)
# ================================
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
SENDGRID_ECHO_TO_STDOUT = True

# ================================
# INSTALLED APPS
# ================================
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'church.apps.ChurchConfig',
    'tithe.apps.TitheConfig',
    
]

# ================================
# MIDDLEWARE
# ================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ================================
# TEMPLATES
# ================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# ================================
# DATABASE (Railway PostgreSQL)
# ================================
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600
    )
}

# ================================
# PASSWORD VALIDATION
# ================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ================================
# INTERNATIONALIZATION
# ================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ================================
# STATIC & MEDIA FILES
# ================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = "tithe.CustomUser"

BASE_URL = os.getenv("BASE_URL", "https://fruitfulyouth.org/")

# ================================
# CACHING
# ================================
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "image-url-cache",
    }
}

# Cache TTL (seconds) for image URL lookups.
IMAGE_URL_CACHE_TTL = int(os.getenv("IMAGE_URL_CACHE_TTL", "3600"))


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "darkly",
    "sidebar_fixed": True,
    "navbar_fixed": True,
    "navbar": "navbar-white navbar-light",
    "sidebar": "sidebar-light-primary",
    "accent": "accent-primary",
}

JAZZMIN_SETTINGS = {
    "site_title": "Fruitful Youth Admin",
    "site_header": "Fruitful Youth",
    "site_brand": "Fruitful Youth",
    "welcome_sign": "Welcome to Fruitful Youth Admin",
    "site_logo": "images/logo.png",
    "site_logo_small": "images/logo.png",
    "site_icon": "images/favicon.ico",
    "site_logo_classes": "brand-image img-circle elevation-2",
    "login_logo": "images/logo.png",
    "login_logo_dark": "images/logo.png",
    "custom_css": "jazzmin/custom_admin.css",
    "show_ui_builder": True,
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
    },
}
