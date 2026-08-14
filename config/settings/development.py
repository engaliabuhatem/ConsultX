from .base import *  # noqa: F401,F403
from .base import BASE_DIR, env

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Local dev only — never used when DJANGO_SETTINGS_MODULE points at production
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
