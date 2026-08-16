import datetime
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Publication

# See apps/careers/tests.py — MEDIA_ROOT is not isolated by the test runner.
_TEST_MEDIA = tempfile.mkdtemp(prefix="consultx-test-media-")


def tearDownModule():
    shutil.rmtree(_TEST_MEDIA, ignore_errors=True)


def make_publication(**overrides):
    defaults = {
        "title": "Seismic Retrofit Guidance",
        "slug": "seismic-retrofit-guidance",
        "abstract": "How to assess existing frames.",
        "published_date": datetime.date(2026, 3, 1),
        "is_published": True,
        "pdf_file": SimpleUploadedFile("doc.pdf", b"%PDF-1.4", content_type="application/pdf"),
    }
    defaults.update(overrides)
    return Publication.objects.create(**defaults)


@override_settings(MEDIA_ROOT=_TEST_MEDIA)
class PublicationListTests(TestCase):
    def test_only_published_documents_are_listed(self):
        make_publication()
        make_publication(title="Draft Report", slug="draft-report", is_published=False)

        response = self.client.get(reverse("publications:list"))
        self.assertContains(response, "Seismic Retrofit Guidance")
        self.assertNotContains(response, "Draft Report")

    def test_category_filter_narrows_the_list(self):
        make_publication(category="whitepaper")
        make_publication(
            title="Bridge Survey", slug="bridge-survey", category="technical_report"
        )

        response = self.client.get(reverse("publications:list"), {"category": "technical_report"})
        self.assertContains(response, "Bridge Survey")
        self.assertNotContains(response, "Seismic Retrofit Guidance")

    def test_empty_state(self):
        response = self.client.get(reverse("publications:list"))
        self.assertContains(response, "No publications yet.")


@override_settings(MEDIA_ROOT=_TEST_MEDIA)
class PublicationDetailTests(TestCase):
    def test_published_document_is_reachable(self):
        pub = make_publication()
        response = self.client.get(reverse("publications:detail", kwargs={"slug": pub.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Seismic Retrofit Guidance")

    def test_draft_is_not_reachable_by_guessing_the_slug(self):
        pub = make_publication(is_published=False)
        response = self.client.get(reverse("publications:detail", kwargs={"slug": pub.slug}))
        self.assertEqual(response.status_code, 404)

    def test_file_extension_label(self):
        self.assertEqual(make_publication().file_extension, "PDF")
