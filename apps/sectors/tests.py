from django.test import TestCase
from django.urls import reverse

from apps.services.models import Service, ServiceCategory

from .models import Sector


class SectorViewTests(TestCase):
    def setUp(self):
        self.sector = Sector.objects.create(
            name="Water & Wastewater", slug="water-wastewater",
            short_description="Treatment plants, networks and reuse schemes.",
            description="Full sector copy.",
        )

    def test_list_shows_sectors(self):
        response = self.client.get(reverse("sectors:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Water &amp; Wastewater")

    def test_detail_renders(self):
        response = self.client.get(reverse("sectors:detail", kwargs={"slug": self.sector.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Full sector copy.")

    def test_detail_lists_related_services(self):
        category = ServiceCategory.objects.create(name="Civil", slug="civil")
        service = Service.objects.create(
            category=category, title="Network Modelling", slug="network-modelling",
            short_description="Hydraulic modelling.", description="...",
        )
        self.sector.related_services.add(service)

        response = self.client.get(reverse("sectors:detail", kwargs={"slug": self.sector.slug}))
        self.assertContains(response, "Network Modelling")

    def test_empty_state(self):
        Sector.objects.all().delete()
        response = self.client.get(reverse("sectors:list"))
        self.assertContains(response, "Sectors will appear here")
