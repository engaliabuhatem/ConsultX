from django.views.generic import ListView, TemplateView

from apps.home.models import StatCounter

from .models import TeamMember


class AboutView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team_preview"] = TeamMember.objects.all()[:4]
        context["stats"] = StatCounter.objects.all()
        return context


class TeamListView(ListView):
    model = TeamMember
    template_name = "pages/team.html"
    context_object_name = "team_members"
