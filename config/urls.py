from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# NOTE: this checkpoint covers models + admin only (see PROJECT_BRIEF.md /
# the delivery note in chat). Public-facing page routes for home, services,
# projects, insights, team, and contact arrive with the frontend pass, and
# will be added here wrapped in i18n_patterns(...) for the EN/AR toggle —
# deliberately not stubbed out ahead of the views that will actually serve
# them.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),  # language switcher endpoint
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
