from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Post


class InsightsViewTests(TestCase):
    def test_list_loads_with_no_posts(self):
        response = self.client.get(reverse("blog:list"))
        self.assertEqual(response.status_code, 200)

    def test_published_post_visible(self):
        Post.objects.create(
            title="Flood Risk in Delta Infrastructure", slug="flood-risk-delta-infrastructure",
            content_type="article", excerpt="Excerpt", content="Content",
            is_published=True, published_at=timezone.now() - timedelta(days=1),
        )
        response = self.client.get(reverse("blog:list"))
        self.assertContains(response, "Flood Risk in Delta Infrastructure")

    def test_future_dated_post_not_visible(self):
        Post.objects.create(
            title="Future Article", slug="future-article", content_type="article",
            excerpt="Excerpt", content="Content",
            is_published=True, published_at=timezone.now() + timedelta(days=1),
        )
        response = self.client.get(reverse("blog:list"))
        self.assertNotContains(response, "Future Article")

    def test_unpublished_post_detail_returns_404(self):
        Post.objects.create(
            title="Draft Whitepaper", slug="draft-whitepaper", content_type="whitepaper",
            excerpt="Excerpt", content="Content", is_published=False,
        )
        response = self.client.get(reverse("blog:detail", kwargs={"slug": "draft-whitepaper"}))
        self.assertEqual(response.status_code, 404)
