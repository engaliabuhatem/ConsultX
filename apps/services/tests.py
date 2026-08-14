from django.test import TestCase
from django.urls import reverse

from .models import Service, ServiceCategory


class ServiceViewTests(TestCase):
    def setUp(self):
        self.structural = ServiceCategory.objects.create(name="Structural", slug="structural", order=1)
        self.mep = ServiceCategory.objects.create(name="MEP", slug="mep", order=2)
        self.service = Service.objects.create(
            category=self.structural, title="Structural Design", slug="structural-design",
            short_description="Short", description="Full description", order=1,
        )
        Service.objects.create(
            category=self.mep, title="MEP Design", slug="mep-design",
            short_description="Short", description="Full", order=2,
        )

    def test_list_view_loads(self):
        response = self.client.get(reverse("services:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Structural Design")
        self.assertContains(response, "MEP Design")

    def test_detail_view_loads(self):
        response = self.client.get(reverse("services:detail", kwargs={"slug": "structural-design"}))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_404_for_unknown_slug(self):
        response = self.client.get(reverse("services:detail", kwargs={"slug": "does-not-exist"}))
        self.assertEqual(response.status_code, 404)

    def test_category_filter_excludes_other_categories(self):
        response = self.client.get(reverse("services:list"), {"category": "structural"})
        self.assertContains(response, "Structural Design")
        self.assertNotContains(response, "MEP Design")
