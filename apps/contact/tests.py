from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from .models import ContactSubmission


class ContactFormTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_valid_submission_saves_and_redirects(self):
        response = self.client.post(reverse("contact:index"), {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "",
            "company": "",
            "service_interest": "",
            "message": "We need help with a flood mitigation study.",
        })
        self.assertRedirects(response, reverse("contact:index"))
        self.assertEqual(ContactSubmission.objects.count(), 1)
        self.assertEqual(ContactSubmission.objects.first().email, "jane@example.com")

    def test_missing_required_field_does_not_save(self):
        response = self.client.post(reverse("contact:index"), {
            "name": "",
            "email": "jane@example.com",
            "message": "Missing my name.",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactSubmission.objects.count(), 0)
        self.assertFormError(response.context["form"], "name", "This field is required.")

    def test_rate_limit_blocks_after_five_submissions_per_ip(self):
        for i in range(5):
            self.client.post(reverse("contact:index"), {
                "name": f"Person {i}", "email": f"p{i}@example.com", "message": "Test message.",
            })
        self.assertEqual(ContactSubmission.objects.count(), 5)

        response = self.client.post(reverse("contact:index"), {
            "name": "One Too Many", "email": "toomany@example.com", "message": "Test message.",
        }, follow=True)
        self.assertEqual(ContactSubmission.objects.count(), 5)
        self.assertContains(response, "Too many submissions")
