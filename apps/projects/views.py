from django.views.generic import DetailView, ListView

from apps.services.models import ServiceCategory

from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = "pages/projects_list.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        qs = Project.objects.filter(is_published=True).select_related("category")
        category_slug = self.request.GET.get("category")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        search = self.request.GET.get("q")
        if search:
            qs = qs.filter(title__icontains=search)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ServiceCategory.objects.all()
        context["active_category"] = self.request.GET.get("category", "")
        context["query"] = self.request.GET.get("q", "")
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "pages/project_detail.html"
    context_object_name = "project"
    queryset = Project.objects.filter(is_published=True)
