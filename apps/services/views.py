from django.views.generic import DetailView, ListView

from .models import Service, ServiceCategory


class ServiceListView(ListView):
    model = Service
    template_name = "pages/services_list.html"
    context_object_name = "services"

    def get_queryset(self):
        qs = Service.objects.select_related("category")
        category_slug = self.request.GET.get("category")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ServiceCategory.objects.all()
        context["active_category"] = self.request.GET.get("category", "")
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = "pages/service_detail.html"
    context_object_name = "service"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.category:
            context["related_projects"] = self.object.category.projects.filter(is_published=True)[:3]
        else:
            context["related_projects"] = []
        return context
