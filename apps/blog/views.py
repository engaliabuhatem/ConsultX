from django.utils import timezone
from django.views.generic import DetailView, ListView

from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "pages/insights_list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        return Post.objects.filter(
            is_published=True, published_at__lte=timezone.now()
        ).select_related("category", "author")


class PostDetailView(DetailView):
    model = Post
    template_name = "pages/insight_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return Post.objects.filter(is_published=True, published_at__lte=timezone.now())
