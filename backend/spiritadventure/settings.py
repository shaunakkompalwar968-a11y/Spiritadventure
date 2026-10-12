"""
Django settings for Spirit Adventures project.
Django 5.x with Django Ninja, WhiteNoise, CORS Headers, and automatic PostgreSQL / SQLite fallback.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-spirit-adventures-super-secret-key-2026")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # Third party apps
    "corsheaders",
    # Local apps
    "api",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "spiritadventure.urls"

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

WSGI_APPLICATION = "spiritadventure.wsgi.application"
ASGI_APPLICATION = "spiritadventure.asgi.application"

# ---------------------------------------------------------------------------
# Database Configuration: PostgreSQL with Automatic SQLite Fallback
# ---------------------------------------------------------------------------
def configure_database():
    database_url = os.getenv("DATABASE_URL")
    db_engine = os.getenv("DB_ENGINE", "").lower()
    db_name = os.getenv("DB_NAME") or os.getenv("POSTGRES_DB")

    sqlite_config = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }

    # If PostgreSQL is explicitly configured or DATABASE_URL is present
    if database_url:
        try:
            import dj_database_url
            parsed = dj_database_url.parse(database_url, conn_max_age=600)
            if parsed and parsed.get("ENGINE") and "postgresql" in parsed.get("ENGINE"):
                # Test if psycopg/psycopg2 is importable
                try:
                    import psycopg  # noqa: F401
                except ImportError:
                    try:
                        import psycopg2  # noqa: F401
                    except ImportError:
                        print("[Database] PostgreSQL requested but neither psycopg nor psycopg2 found. Falling back to SQLite.")
                        return sqlite_config

                print("[Database] Using PostgreSQL via DATABASE_URL.")
                return parsed
        except Exception as e:
            print(f"[Database] Failed to configure DATABASE_URL: {e}. Falling back to SQLite.")
            return sqlite_config

    elif db_engine == "postgresql" or db_name:
        try:
            import psycopg  # noqa: F401
            postgres_config = {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": db_name or "spiritadventure",
                "USER": os.getenv("DB_USER", "postgres"),
                "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
                "HOST": os.getenv("DB_HOST", "localhost"),
                "PORT": os.getenv("DB_PORT", "5432"),
            }
            print("[Database] Using PostgreSQL configuration.")
            return postgres_config
        except Exception as e:
            print(f"[Database] PostgreSQL error: {e}. Automatically falling back to SQLite.")
            return sqlite_config

    print("[Database] No PostgreSQL config detected. Using default SQLite.")
    return sqlite_config

DATABASES = {
    "default": configure_database()
}

# Password validation
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
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images) with WhiteNoise
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise compressed storage for production
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# CORS Configuration
# ---------------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL", "True").lower() in ("true", "1", "yes")

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

cors_extra = os.getenv("CORS_ALLOWED_ORIGINS", "")
if cors_extra:
    for origin in cors_extra.split(","):
        trimmed = origin.strip()
        if trimmed and trimmed not in CORS_ALLOWED_ORIGINS:
            CORS_ALLOWED_ORIGINS.append(trimmed)

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
