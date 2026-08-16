"""
Base settings shared by every environment.

Environment-specific values (secrets, hosts, database credentials) are never
hardcoded here — they come from environment variables via django-environ,
loaded from a local .env file in development and from the real environment
in production. See .env.example for the full list of variables.
"""

from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])

INSTALLED_APPS = [
    # Admin theme must be listed before django.contrib.admin
    "unfold",
    "unfold.contrib.filters",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # ConsultX apps
    "apps.core",
    "apps.siteconfig",
    "apps.home",
    "apps.services",
    "apps.sectors",
    "apps.projects",
    "apps.team",
    "apps.testimonials",
    "apps.blog",
    "apps.publications",
    "apps.careers",
    "apps.partners",
    "apps.contact",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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
                "django.template.context_processors.i18n",
                "apps.siteconfig.context_processors.site_settings",
                "apps.core.navigation.navigation",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization — English primary, Arabic as a toggle (see PROJECT_BRIEF.md §7)
LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", "English"),
    ("ar", "Arabic"),
]
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = env("DJANGO_TIME_ZONE", default="Africa/Cairo")
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Contact form throttling target (django-ratelimit) — wired up in apps.contact next pass
CONTACT_FORM_RATE = "5/h"

UNFOLD = {
    "SITE_TITLE": "ConsultX Admin",
    "SITE_HEADER": "ConsultX",
    "SITE_SUBHEADER": "Content & Enquiries",
    "SITE_SYMBOL": "engineering",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "BORDER_RADIUS": "6px",
    # Computed from the actual brand hex values (accent #d6481f, graphite hue-matched
    # rather than taken from the near-black graphite hex directly — a source color that
    # dark carries almost no reliable hue information, so its OKLCH hue comes out
    # essentially as noise). Regenerate with a proper color library if the palette
    # in PROJECT_BRIEF.md item 4 gets reconfirmed to something else.
    "COLORS": {
        "base": {
            "50": "oklch(98.0% 0.006 35.9)",
            "100": "oklch(95.5% 0.007 35.9)",
            "200": "oklch(90.0% 0.008 35.9)",
            "300": "oklch(82.0% 0.009 35.9)",
            "400": "oklch(71.0% 0.010 35.9)",
            "500": "oklch(60.0% 0.010 35.9)",
            "600": "oklch(50.0% 0.009 35.9)",
            "700": "oklch(42.0% 0.008 35.9)",
            "800": "oklch(33.0% 0.007 35.9)",
            "900": "oklch(24.0% 0.006 35.9)",
            "950": "oklch(15.0% 0.005 35.9)",
        },
        "primary": {
            "50": "oklch(97.5% 0.020 35.9)",
            "100": "oklch(94.0% 0.040 35.9)",
            "200": "oklch(87.0% 0.070 35.9)",
            "300": "oklch(79.0% 0.110 35.9)",
            "400": "oklch(68.5% 0.150 35.9)",
            "500": "oklch(59.6% 0.185 35.9)",
            "600": "oklch(52.0% 0.170 35.9)",
            "700": "oklch(44.0% 0.145 35.9)",
            "800": "oklch(36.5% 0.115 35.9)",
            "900": "oklch(30.0% 0.085 35.9)",
            "950": "oklch(21.0% 0.055 35.9)",
        },
    },
}
