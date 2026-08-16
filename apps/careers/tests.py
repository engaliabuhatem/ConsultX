import datetime

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import JobApplication, JobOpening


def make_cv(name="cv.pdf", content=b"%PDF-1.4 fake"):
    return SimpleUploadedFile(name, content, content_type="application/pdf")


def valid_payload(**overrides):
    data = {
        "full_name": "Amira Hassan",
        "email": "amira@example.com",
        "phone": "+20 100 000 0000",
        "location": "Cairo, Egypt",
        "years_experience": 7,
        "current_employer": "Nile Engineering",
        "notice_period": "1 month",
        "expected_salary": "",
        "linkedin_url": "",
        "portfolio_url": "",
        "cover_note": "I lead structural reviews on water infrastructure.",
        "heard_about": "LinkedIn",
        "consent": "on",
    }
    data.update(overrides)
    return data


class JobOpeningListTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_only_open_roles_are_listed(self):
        JobOpening.objects.create(
            title="Structural Engineer", slug="structural-engineer",
            location="Cairo", summary="Design and review.", description="...", is_open=True,
        )
        JobOpening.objects.create(
            title="Retired Role", slug="retired-role",
            location="Cairo", summary="Old.", description="...", is_open=False,
        )
        response = self.client.get(reverse("careers:list"))
        self.assertContains(response, "Structural Engineer")
        self.assertNotContains(response, "Retired Role")

    def test_empty_state_still_offers_speculative_application(self):
        response = self.client.get(reverse("careers:list"))
        self.assertContains(response, "No open roles right now.")
        self.assertContains(response, reverse("careers:apply"))


class JobApplicationSubmitTests(TestCase):
    def setUp(self):
        cache.clear()
        self.opening = JobOpening.objects.create(
            title="Structural Engineer", slug="structural-engineer",
            location="Cairo", summary="Design and review.", description="...", is_open=True,
        )
        self.url = reverse("careers:detail", kwargs={"slug": self.opening.slug})

    def test_valid_application_is_saved_against_the_role(self):
        response = self.client.post(self.url, valid_payload(cv_file=make_cv()))
        self.assertRedirects(response, self.url)

        application = JobApplication.objects.get()
        self.assertEqual(application.full_name, "Amira Hassan")
        self.assertEqual(application.position, self.opening)
        # Title is snapshotted so the record survives the role being deleted.
        self.assertEqual(application.position_title, "Structural Engineer")

    def test_position_title_survives_role_deletion(self):
        self.client.post(self.url, valid_payload(cv_file=make_cv()))
        self.opening.delete()

        application = JobApplication.objects.get()
        self.assertIsNone(application.position)
        self.assertEqual(application.position_title, "Structural Engineer")

    def test_speculative_application_has_no_position(self):
        response = self.client.post(reverse("careers:apply"), valid_payload(cv_file=make_cv()))
        self.assertRedirects(response, reverse("careers:apply"))

        application = JobApplication.objects.get()
        self.assertIsNone(application.position)
        self.assertEqual(application.position_title, "")

    def test_consent_is_required(self):
        payload = valid_payload(cv_file=make_cv())
        del payload["consent"]
        response = self.client.post(self.url, payload)

        self.assertEqual(JobApplication.objects.count(), 0)
        self.assertContains(response, "without this consent")

    def test_cv_is_required(self):
        response = self.client.post(self.url, valid_payload())
        self.assertEqual(JobApplication.objects.count(), 0)
        self.assertFormError(response.context["form"], "cv_file", "This field is required.")

    def test_cv_extension_is_validated(self):
        bad = SimpleUploadedFile("cv.exe", b"MZ", content_type="application/octet-stream")
        response = self.client.post(self.url, valid_payload(cv_file=bad))

        self.assertEqual(JobApplication.objects.count(), 0)
        self.assertFormError(response.context["form"], "cv_file", "Upload a PDF, DOC or DOCX file.")

    def test_cover_letter_or_note_is_required(self):
        response = self.client.post(self.url, valid_payload(cv_file=make_cv(), cover_note=""))

        self.assertEqual(JobApplication.objects.count(), 0)
        self.assertFormError(
            response.context["form"], "cover_note",
            "Please attach a cover letter or write a short note.",
        )

    def test_attached_cover_letter_satisfies_the_requirement(self):
        letter = SimpleUploadedFile("letter.pdf", b"%PDF-1.4", content_type="application/pdf")
        response = self.client.post(
            self.url, valid_payload(cv_file=make_cv(), cover_note="", cover_letter_file=letter)
        )
        self.assertRedirects(response, self.url)
        self.assertEqual(JobApplication.objects.count(), 1)

    def test_rate_limit_blocks_the_sixth_application(self):
        for _ in range(5):
            self.client.post(self.url, valid_payload(cv_file=make_cv()))
        self.assertEqual(JobApplication.objects.count(), 5)

        self.client.post(self.url, valid_payload(cv_file=make_cv()))
        self.assertEqual(JobApplication.objects.count(), 5)


class ClosedRoleTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_closed_role_is_not_reachable(self):
        opening = JobOpening.objects.create(
            title="Closed", slug="closed", location="Cairo",
            summary="s", description="d", is_open=False,
        )
        response = self.client.get(reverse("careers:detail", kwargs={"slug": opening.slug}))
        self.assertEqual(response.status_code, 404)

    def test_past_closing_date_hides_the_form_but_keeps_the_page(self):
        opening = JobOpening.objects.create(
            title="Expired", slug="expired", location="Cairo",
            summary="s", description="d", is_open=True,
            closing_date=timezone.localdate() - datetime.timedelta(days=1),
        )
        response = self.client.get(reverse("careers:detail", kwargs={"slug": opening.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["form"])
        self.assertContains(response, "This role has closed.")

    def test_requirement_list_splits_on_newlines(self):
        opening = JobOpening.objects.create(
            title="R", slug="r", location="Cairo", summary="s", description="d",
            requirements="BSc Civil Engineering\n\n  5 years experience  \n",
        )
        self.assertEqual(
            opening.requirement_list,
            ["BSc Civil Engineering", "5 years experience"],
        )
