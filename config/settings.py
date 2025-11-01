from pathlib import Path
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env برای توسعه محلی
# این خط در سرور (Liara) تاثیری ندارد چون فایل .env وجود ندارد
# و متغیرها مستقیما از پنل لیارا خوانده می شوند.
load_dotenv()

# مسیر پایه پروژه
BASE_DIR = Path(__file__).resolve().parent.parent

# کلید مخفی برنامه از متغیر محیطی خوانده می شود که بسیار امن است.
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-dev-key"  # این فقط یک مقدار پیش فرض برای توسعه محلی است
)

# تشخیص محیط اجرا (توسعه یا پروداکشن)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# حالت دیباگ فقط در محیط توسعه فعال است. در پروداکشن حتما False باشد.
DEBUG = os.getenv("DEBUG", "True") == "True"

# برای Liara همه هاست‌ها را مجاز می کنیم چون دامنه ممکن است تغییر کند.
ALLOWED_HOSTS = ["*"]
# منابعی که می توانند درخواست CSRF ارسال کنند (برای امنیت در Liara ضروری است)
CSRF_TRUSTED_ORIGINS = ["https://*.liara.run", "https://*.liara.ir"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "myblog",      # اپلیکیشن های سفارشی شما
    "account",     # اپلیکیشن های سفارشی شما
]

MIDDLEWARE = [
    # این میدل‌ور باید همیشه اول باشد
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise برای سرویس فایل‌های استاتیک در پروداکشن (بسیار مهم)
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
        "DIRS": [BASE_DIR / "templates"],  # پوشه قالب‌های سراسری
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
# پایگاه داده برای Liara (بخش بسیار مهم)
# -----------------------------
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # اگر DATABASE_URL تنظیم شده باشد (در پروداکشن)، از آن برای اتصال به PostgreSQL استفاده کن
    import dj_database_url
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    # در غیر این صورت (توسعه محلی)، از SQLite استفاده کن
    # در Liara همیشه از مسیر /tmp استفاده کنید چون این تنها مسیری است که دائمی است
    db_path = "/tmp/db.sqlite3"
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": db_path,
        }
    }
    # فقط برای حالت SQLite، پوشه مربوطه را در صورت عدم وجود بساز
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

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

# -----------------------------
# فایل‌های استاتیک و مدیا برای Liara
# -----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = "/tmp/staticfiles"  # در Liara فایل‌های استاتیک در این مسیر جمع آوری می شوند
STATICFILES_DIRS = [BASE_DIR / "static"]  # پوشه استاتیک پروژه

MEDIA_URL = "/media/"
MEDIA_ROOT = "/tmp/media"  # در Liara فایل‌های آپلود شده در این مسیر ذخیره می شوند

# تنظیمات WhiteNoise برای بهینه‌سازی فایل‌های استاتیک در پروداکشن
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "post_list"
LOGOUT_REDIRECT_URL = "post_list"

# -----------------------------
# تنظیمات امنیتی برای پروداکشن
# -----------------------------
if ENVIRONMENT == "production":
    # این تنظیمات امنیتی فقط در محیط پروداکشن فعال می شوند
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    # این خط برای پلتفرم‌هایی مانند لیارا که از پروکسی SSL استفاده می کنند، حیاتی است
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    # در محیط توسعه این تنظیمات خاموش هستند
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

# ایجاد پوشه‌های لازم در صورت عدم وجود (برای جلوگیری از خطا)
os.makedirs(STATIC_ROOT, exist_ok=True)
os.makedirs(MEDIA_ROOT, exist_ok=True)