from django.views.generic import DetailView, ListView

from .models import Publication


class PublicationListView(ListView):
    model = Publication
    template_name = "pages/publications_list.html"
    context_object_name = "publications"
    paginate_by = 12

    def get_queryset(self):
        qs = Publication.objects.filter(is_published=True).prefetch_related("authors")
        category = self.request.GET.get("category")
        if category:
            qs = qs.filter(category=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Publication.CATEGORY_CHOICES
        context["active_category"] = self.request.GET.get("category", "")
        return context


class PublicationDetailView(DetailView):
    model = Publication
    template_name = "pages/publication_detail.html"
    context_object_name = "publication"

    def get_queryset(self):
        # Drafts must not be reachable by guessing the slug.
        return Publication.objects.filter(is_published=True).prefetch_related("authors")
