from django.views.generic import DetailView, ListView

from .models import Sector


class SectorListView(ListView):
    model = Sector
    template_name = "pages/sectors_list.html"
    context_object_name = "sectors"


class SectorDetailView(DetailView):
    model = Sector
    template_name = "pages/sector_detail.html"
    context_object_name = "sector"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_services"] = self.object.related_services.select_related("category")
        return context
