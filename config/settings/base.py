"""
Base settings shared by every environment.

Environment-specific values (secrets, hosts, database credentials) are never
hardcoded here — they come from environment variables via django-environ,
loaded from a local .env file in development and from the real environment
in production. See .env.example for the full list of variables.
"""

from pathlib import Path

import environ

from adminkit.nav import dashboard_item, group, item
from adminkit.theme import build_unfold

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])

INSTALLED_APPS = [
    # Admin theme must be listed before django.contrib.admin. adminkit precedes
    # unfold in turn, so its admin/index.html overrides Unfold's.
    "adminkit",
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

# --- Admin theme -----------------------------------------------------------
# Everything reusable lives in the adminkit app; only what is specific to
# ConsultX stays here. Sections are grouped the way the site itself is
# organised, not the way Django groups by app label — someone editing the
# homepage should not have to know that the hero and the CTA banner live in one
# app while the services they link to live in another.
ADMIN_NAVIGATION = [
    group("Overview", [
        dashboard_item(),
        item("siteconfig.SiteSettings", "Site settings", icon="tune"),
    ]),
    group("Homepage", [
        item("home.HomeHero", "Hero section", icon="landscape"),
        item("home.PracticeChapter", "Chapters", icon="view_carousel"),
        item("home.StatCounter", "Stat counters", icon="trending_up"),
        item("home.CTABanner", "CTA banner", icon="campaign"),
    ]),
    group("Expertise", [
        item("services.Service", "Services", icon="engineering"),
        item("services.ServiceCategory", "Service categories", icon="category"),
        item("sectors.Sector", "Sectors", icon="domain"),
        item("projects.Project", "Projects", icon="architecture"),
    ]),
    group("People & voice", [
        item("team.TeamMember", "Team", icon="groups"),
        item("testimonials.Testimonial", "Testimonials", icon="format_quote"),
        item("blog.Post", "Insights", icon="article"),
        item("publications.Publication", "Publications", icon="menu_book"),
    ]),
    group("Inbox", [
        item("contact.ContactSubmission", "Enquiries", icon="mail"),
        item("careers.JobOpening", "Job openings", icon="work"),
        item("careers.JobApplication", "Job applications", icon="how_to_reg"),
        item("partners.PartnerApplication", "Partner applications", icon="handshake"),
    ]),
]

# brand/neutral drive the whole Unfold color ramp — see adminkit/palette.py.
# Clay rather than gold as the accent because Unfold paints white text on
# primary-600, and gold at any usable lightness cannot carry white text. Gold is
# applied deliberately, on dark surfaces only, via static/css/admin-brand.css.
UNFOLD = build_unfold(
    title="ConsultX Admin",
    header="ConsultX",
    subheader="Content & Enquiries",
    site_symbol="engineering",
    brand="#9c5539",   # brick clay
    neutral="#f2efe4",  # warm paper — keeps admin greys warm, matching the site
    navigation=ADMIN_NAVIGATION,
    dashboard_callback="apps.core.dashboard.dashboard_callback",
    login_image="img/chapter-sustainability.jpg",
    extra_styles=["css/admin-brand.css"],
)
