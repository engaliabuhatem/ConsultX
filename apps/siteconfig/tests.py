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
