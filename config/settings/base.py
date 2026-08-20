"""
Base settings shared by every environment.

Environment-specific values (secrets, hosts, database credentials) are never
hardcoded here — they come from environment variables via django-environ,
loaded from a local .env file in development and from the real environment
in production. See .env.example for the full list of variables.
"""

from pathlib import Path

import environ
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

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
    "SITE_URL": "/",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,
    "BORDER_RADIUS": "8px",
    "DASHBOARD_CALLBACK": "apps.core.dashboard.dashboard_callback",
    # Brand chrome the COLORS ramps below can't express: the tri-color
    # practice bar, gold focus rings, the display face, and the dashboard
    # components in templates/admin/index.html.
    "STYLES": [lambda request: static("css/admin.css")],
    # Computed from the site's own palette (assets/input.css) by converting
    # each brand hex to OKLCH and holding its hue constant down the ramp:
    #
    #   primary  brick clay  #9c5539  ->  L 52.8%  C 0.103  H 41.8
    #   base     warm paper  #f2efe4  ->  L 95.1%  C 0.015  H 94.2
    #
    # Clay rather than gold for primary because Unfold paints white text on
    # primary-600 — gold at any usable lightness cannot carry white text.
    # Gold is applied deliberately, on dark surfaces only, in admin.css.
    # The base ramp keeps the paper hue so admin greys read warm, matching
    # the site instead of the default cool blue-grey.
    "COLORS": {
        "base": {
            "50": "oklch(98.4% 0.006 94.2)",
            "100": "oklch(96.2% 0.008 94.2)",
            "200": "oklch(92.4% 0.010 94.2)",
            "300": "oklch(86.5% 0.011 94.2)",
            "400": "oklch(72.0% 0.012 94.2)",
            "500": "oklch(58.5% 0.012 94.2)",
            "600": "oklch(47.5% 0.011 94.2)",
            "700": "oklch(39.5% 0.010 96.0)",
            "800": "oklch(30.0% 0.009 100.0)",
            "900": "oklch(22.0% 0.010 104.0)",
            "950": "oklch(15.5% 0.010 107.4)",
        },
        "primary": {
            "50": "oklch(97.2% 0.014 41.8)",
            "100": "oklch(94.0% 0.030 41.8)",
            "200": "oklch(88.5% 0.055 41.8)",
            "300": "oklch(80.0% 0.085 41.8)",
            "400": "oklch(66.5% 0.105 41.8)",
            "500": "oklch(58.0% 0.115 41.8)",
            "600": "oklch(52.8% 0.103 41.8)",
            "700": "oklch(45.0% 0.090 41.8)",
            "800": "oklch(37.5% 0.074 41.8)",
            "900": "oklch(31.5% 0.060 41.8)",
            "950": "oklch(22.0% 0.042 41.8)",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        # Grouped the way the site itself is organised, not the way Django
        # groups by app label — someone editing the homepage should not have
        # to know that the hero and the CTA banner live in one app while the
        # services they link to live in another.
        "navigation": [
            {
                "title": _("Overview"),
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": _("Site settings"),
                        "icon": "tune",
                        "link": reverse_lazy("admin:siteconfig_sitesettings_changelist"),
                    },
                ],
            },
            {
                "title": _("Homepage"),
                "items": [
                    {
                        "title": _("Hero section"),
                        "icon": "landscape",
                        "link": reverse_lazy("admin:home_homehero_changelist"),
                    },
                    {
                        "title": _("Chapters"),
                        "icon": "view_carousel",
                        "link": reverse_lazy("admin:home_practicechapter_changelist"),
                    },
                    {
                        "title": _("Stat counters"),
                        "icon": "trending_up",
                        "link": reverse_lazy("admin:home_statcounter_changelist"),
                    },
                    {
                        "title": _("CTA banner"),
                        "icon": "campaign",
                        "link": reverse_lazy("admin:home_ctabanner_changelist"),
                    },
                ],
            },
            {
                "title": _("Expertise"),
                "items": [
                    {
                        "title": _("Services"),
                        "icon": "engineering",
                        "link": reverse_lazy("admin:services_service_changelist"),
                    },
                    {
                        "title": _("Service categories"),
                        "icon": "category",
                        "link": reverse_lazy("admin:services_servicecategory_changelist"),
                    },
                    {
                        "title": _("Sectors"),
                        "icon": "domain",
                        "link": reverse_lazy("admin:sectors_sector_changelist"),
                    },
                    {
                        "title": _("Projects"),
                        "icon": "architecture",
                        "link": reverse_lazy("admin:projects_project_changelist"),
                    },
                ],
            },
            {
                "title": _("People & voice"),
                "items": [
                    {
                        "title": _("Team"),
                        "icon": "groups",
                        "link": reverse_lazy("admin:team_teammember_changelist"),
                    },
                    {
                        "title": _("Testimonials"),
                        "icon": "format_quote",
                        "link": reverse_lazy("admin:testimonials_testimonial_changelist"),
                    },
                    {
                        "title": _("Insights"),
                        "icon": "article",
                        "link": reverse_lazy("admin:blog_post_changelist"),
                    },
                    {
                        "title": _("Publications"),
                        "icon": "menu_book",
                        "link": reverse_lazy("admin:publications_publication_changelist"),
                    },
                ],
            },
            {
                "title": _("Inbox"),
                "items": [
                    {
                        "title": _("Enquiries"),
                        "icon": "mail",
                        "link": reverse_lazy("admin:contact_contactsubmission_changelist"),
                    },
                    {
                        "title": _("Job openings"),
                        "icon": "work",
                        "link": reverse_lazy("admin:careers_jobopening_changelist"),
                    },
                    {
                        "title": _("Job applications"),
                        "icon": "how_to_reg",
                        "link": reverse_lazy("admin:careers_jobapplication_changelist"),
                    },
                    {
                        "title": _("Partner applications"),
                        "icon": "handshake",
                        "link": reverse_lazy("admin:partners_partnerapplication_changelist"),
                    },
                ],
            },
        ],
    },
    "LOGIN": {
        "image": lambda request: static("img/chapter-sustainability.jpg"),
    },
}
