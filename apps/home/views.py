from django.views.generic import TemplateView

from apps.home.models import DEFAULT_CHAPTERS, CTABanner, HomeHero, PracticeChapter, StatCounter
from apps.projects.models import Project
from apps.services.models import Service
from apps.testimonials.models import Testimonial


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hero"] = HomeHero.objects.first()
        context["stats"] = StatCounter.objects.all()
        context["featured_services"] = Service.objects.filter(is_featured=True).select_related("category")[:3]
        context["featured_projects"] = Project.objects.filter(is_published=True)[:2]
        context["testimonials"] = Testimonial.objects.filter(is_published=True)[:3]
        context["cta"] = CTABanner.objects.first()

        # The designed chapter bands. Migration 0004 seeds the comp's three,
        # so normally this is just the queryset; DEFAULT_CHAPTERS is the
        # safety net for an install where someone has deleted every row —
        # three empty gaps down the homepage is not a state worth shipping.
        # Both shapes support the same template lookups (dict keys and model
        # attributes resolve identically).
        chapters = list(PracticeChapter.objects.all())
        context["chapters"] = chapters or DEFAULT_CHAPTERS

        # The header sits *over* the hero here rather than above it, so it
        # starts transparent and only turns solid once the page scrolls.
        context["nav_overlay"] = True
        return context
