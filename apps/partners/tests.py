from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import PartnerApplication


def valid_payload(**overrides):
    data = {
        "company_name": "Delta Geotechnical",
        "registration_number": "CR-99887",
        "tax_id": "",
        "website": "https://example.com",
        "country": "Egypt",
        "city": "Alexandria",
        "year_established": 2011,
        "employee_count": "11-50",
        "contact_name": "Omar Fahmy",
        "contact_title": "Managing Director",
        "contact_email": "omar@example.com",
        "contact_phone": "+20 100 000 0000",
        "partnership_type": "subconsultant",
        "capabilities": "Ground investigation, pile design, slope stability.",
        "key_clients": "",
        "annual_turnover": "",
        "certifications": "ISO 9001",
        "message": "",
        "consent": "on",
    }
    data.update(overrides)
    return data


class PartnerFormTests(TestCase):
    def setUp(self):
        cache.clear()
        self.url = reverse("partners:index")

    def test_page_renders_with_the_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Become a Partner")
        self.assertContains(response, 'enctype="multipart/form-data"')

    def test_valid_registration_is_saved(self):
        response = self.client.post(self.url, valid_payload())
        self.assertRedirects(response, self.url)

        application = PartnerApplication.objects.get()
        self.assertEqual(application.company_name, "Delta Geotechnical")
        self.assertEqual(application.status, "new")

    def test_consent_is_required(self):
        payload = valid_payload()
        del payload["consent"]
        response = self.client.post(self.url, payload)

        self.assertEqual(PartnerApplication.objects.count(), 0)
        self.assertContains(response, "without this consent")

    def test_declared_conflict_requires_details(self):
        response = self.client.post(self.url, valid_payload(has_conflict_of_interest="on"))

        self.assertEqual(PartnerApplication.objects.count(), 0)
        self.assertFormError(
            response.context["form"], "conflict_details",
            "Please describe the conflict you are declaring.",
        )

    def test_declared_conflict_with_details_is_accepted(self):
        response = self.client.post(self.url, valid_payload(
            has_conflict_of_interest="on",
            conflict_details="Shared director with a current ConsultX client.",
        ))
        self.assertRedirects(response, self.url)
        self.assertEqual(PartnerApplication.objects.count(), 1)

    def test_undeclared_conflict_needs_no_details(self):
        response = self.client.post(self.url, valid_payload())
        self.assertRedirects(response, self.url)
        self.assertFalse(PartnerApplication.objects.get().has_conflict_of_interest)

    def test_future_year_established_is_rejected(self):
        next_year = timezone.localdate().year + 1
        response = self.client.post(self.url, valid_payload(year_established=next_year))

        self.assertEqual(PartnerApplication.objects.count(), 0)
        self.assertFormError(
            response.context["form"], "year_established", "That year is in the future."
        )

    def test_rate_limit_blocks_the_sixth_submission(self):
        for _ in range(5):
            self.client.post(self.url, valid_payload())
        self.assertEqual(PartnerApplication.objects.count(), 5)

        self.client.post(self.url, valid_payload())
        self.assertEqual(PartnerApplication.objects.count(), 5)


class PartnerAccessibilityTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_field_errors_are_wired_to_their_input(self):
        """A rendered error must be announced, not just coloured."""
        response = self.client.post(reverse("partners:index"), valid_payload(company_name=""))
        html = response.content.decode()

        self.assertIn('id="id_company_name_error"', html)
        self.assertIn('aria-describedby="id_company_name_error"', html)
        self.assertIn('aria-invalid="true"', html)
        self.assertIn('role="alert"', html)
