from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),  # language switcher endpoint
]

# English unprefixed (primary), Arabic at /ar/... (toggle) — per
# PROJECT_BRIEF.md §7, which overrides the build prompt's Arabic-primary default.
urlpatterns += i18n_patterns(
    path("", include("apps.home.urls")),
    path("", include("apps.team.urls")),
    path("services/", include("apps.services.urls")),
    path("sectors/", include("apps.sectors.urls")),
    path("projects/", include("apps.projects.urls")),
    path("insights/", include("apps.blog.urls")),
    path("publications/", include("apps.publications.urls")),
    path("careers/", include("apps.careers.urls")),
    path("partners/", include("apps.partners.urls")),
    path("contact/", include("apps.contact.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
