from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    def test_home_page_loads_on_empty_database(self):
        """Nothing seeded — must render gracefully, not 500."""
        response = self.client.get(reverse("home:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/home.html")


class LanguageToggleTests(TestCase):
    def test_english_is_default_and_unprefixed(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'dir="ltr"')

    def test_arabic_prefix_serves_rtl(self):
        response = self.client.get("/ar/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'dir="rtl"')
