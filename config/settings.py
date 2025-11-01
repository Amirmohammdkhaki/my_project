from pathlib import Path
import os
from dotenv import load_dotenv

# بارگذاری .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-dev-key"
)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "True") == "True"

# برای Liara همه هاست‌ها را允许 کنید
ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ["https://*.liara.run", "https://*.liara.ir"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "myblog",
    "account",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

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
            ],
        },
    },
]

# -----------------------------
# پایگاه داده برای Liara
# -----------------------------
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    import dj_database_url
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    # در Liara همیشه از مسیر /tmp استفاده کنید
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "/tmp/db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fa-ir"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = "/tmp/staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = "/tmp/media"

# WhiteNoise configuration
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "post_list"
LOGOUT_REDIRECT_URL = "post_list"

# تنظیمات امنیتی
if ENVIRONMENT == "production":
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

# ایجاد پوشه‌های لازم
os.makedirs(STATIC_ROOT, exist_ok=True)
os.makedirs(MEDIA_ROOT, exist_ok=True)
os.makedirs(os.path.dirname(DATABASES['default']['NAME']), exist_ok=True)