from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import SiteSettings


class SiteSettingsSingletonTests(TestCase):
    def test_seed_migration_created_exactly_one_row(self):
        self.assertEqual(SiteSettings.objects.count(), 1)

    def test_load_returns_the_same_instance(self):
        first = SiteSettings.load()
        second = SiteSettings.load()
        self.assertEqual(first.pk, second.pk)

    def test_cannot_create_a_second_row(self):
        with self.assertRaises(ValidationError):
            SiteSettings.objects.create()


class CustomCSSTests(TestCase):
    """Free-form styling escape hatch. The one thing that has to keep working: '&'
    and other ordinary CSS characters must render unescaped; the one thing that has
    to keep failing: anything containing '<', which could close the <style> tag."""

    def test_ordinary_css_with_ampersand_renders_unescaped(self):
        settings_obj = SiteSettings.load()
        settings_obj.custom_css = 'body::after { content: "A & B"; }'
        settings_obj.save()

        response = self.client.get("/")
        self.assertContains(response, 'content: "A & B"')

    def test_style_tag_breakout_is_rejected(self):
        settings_obj = SiteSettings.load()
        settings_obj.custom_css = "body{color:red}</style><script>alert(1)</script>"
        with self.assertRaises(ValidationError):
            settings_obj.full_clean()

    def test_blank_means_no_style_tag_rendered(self):
        settings_obj = SiteSettings.load()
        settings_obj.custom_css = ""
        settings_obj.save()

        response = self.client.get("/")
        self.assertNotContains(response, "site_settings.custom_css")


class AccentColorOverrideTests(TestCase):
    """The one styling control that's actually admin-editable — see chat: this is
    what makes 'let staff change the site's color from the admin panel' real."""

    def test_valid_hex_saves_and_appears_on_every_page(self):
        settings_obj = SiteSettings.load()
        settings_obj.accent_color = "#1e40af"
        settings_obj.save()

        response = self.client.get("/")
        self.assertContains(response, "--color-accent: #1e40af")

    def test_blank_means_no_override_rendered(self):
        settings_obj = SiteSettings.load()
        settings_obj.accent_color = ""
        settings_obj.save()

        response = self.client.get("/")
        self.assertNotContains(response, "--color-accent:")

    def test_invalid_hex_is_rejected(self):
        settings_obj = SiteSettings.load()
        settings_obj.accent_color = "not-a-color"
        with self.assertRaises(ValidationError):
            settings_obj.full_clean()
