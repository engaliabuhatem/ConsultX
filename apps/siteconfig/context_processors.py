from .models import SiteSettings


def site_settings(request):
    """Exposes {{ site_settings.* }} in every template without per-view boilerplate."""
    return {"site_settings": SiteSettings.load()}
