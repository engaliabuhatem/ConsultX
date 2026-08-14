from django.views.generic import TemplateView

from apps.home.models import CTABanner, HomeHero, StatCounter
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
        return context
