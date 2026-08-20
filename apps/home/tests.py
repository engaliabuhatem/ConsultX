from django.test import TestCase
from django.urls import reverse

from apps.home.models import DEFAULT_CHAPTERS, PracticeChapter


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


class PracticeChapterTests(TestCase):
    """The three chapter bands are the spine of the homepage design, so the
    two ways they can be sourced both need to hold up."""

    def test_seeded_chapters_render(self):
        """Migration 0004 puts the comp's three chapters in the database."""
        response = self.client.get(reverse("home:index"))
        self.assertEqual(PracticeChapter.objects.count(), 3)
        for chapter in PracticeChapter.objects.all():
            self.assertContains(response, chapter.title)

    def test_falls_back_to_defaults_when_table_emptied(self):
        """Deleting every row must not leave three empty bands on the page."""
        PracticeChapter.objects.all().delete()
        response = self.client.get(reverse("home:index"))
        self.assertEqual(response.status_code, 200)
        for default in DEFAULT_CHAPTERS:
            self.assertContains(response, default["title"])

    def test_chapter_without_upload_still_has_art(self):
        """An unfilled image field falls through to the palette's stock shot
        rather than rendering a flat black band."""
        for chapter in PracticeChapter.objects.all():
            self.assertFalse(chapter.image)
            self.assertTrue(chapter.static_image)

        response = self.client.get(reverse("home:index"))
        self.assertContains(response, "img/chapter-sustainability.jpg")
        self.assertContains(response, "img/chapter-infrastructure.jpg")
        self.assertContains(response, "img/chapter-hydraulic.jpg")


class NavOverlayTests(TestCase):
    """The header only overlays a hero on the homepage; anywhere else a
    transparent bar would be invisible against the paper background."""

    def test_home_marks_the_header_as_an_overlay(self):
        response = self.client.get(reverse("home:index"))
        self.assertTrue(response.context["nav_overlay"])
        self.assertContains(response, "fixed top-0 inset-x-0")
        self.assertNotContains(response, "sticky top-0 inset-x-0")

    def test_inner_page_gets_the_solid_header(self):
        response = self.client.get(reverse("services:list"))
        self.assertIsNone(response.context.get("nav_overlay"))
        self.assertContains(response, "site-header-solid")
