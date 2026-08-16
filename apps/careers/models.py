from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.core.models import SEOFields, TimeStampedModel
from apps.core.validators import DOCUMENT_VALIDATORS


class JobOpening(TimeStampedModel, SEOFields):
    """A published vacancy. Applications may also arrive with no opening
    attached (speculative), so JobApplication.position is nullable."""

    EMPLOYMENT_TYPE_CHOICES = [
        ("full_time", "Full time"),
        ("part_time", "Part time"),
        ("contract", "Contract"),
        ("internship", "Internship"),
    ]
    WORKPLACE_CHOICES = [
        ("on_site", "On site"),
        ("hybrid", "Hybrid"),
        ("remote", "Remote"),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    department = models.CharField(max_length=100, blank=True, help_text='e.g. "Structural Engineering"')
    location = models.CharField(max_length=120, help_text='e.g. "Cairo, Egypt"')
    workplace_type = models.CharField(max_length=10, choices=WORKPLACE_CHOICES, default="on_site")
    employment_type = models.CharField(
        max_length=12, choices=EMPLOYMENT_TYPE_CHOICES, default="full_time"
    )
    summary = models.CharField(max_length=250, help_text="One-line teaser shown on the careers grid.")
    description = models.TextField(help_text="Role, responsibilities, reporting line.")
    requirements = models.TextField(blank=True, help_text="One requirement per line.")
    is_open = models.BooleanField(
        default=False,
        help_text="Off by default. Closed roles stay listed but stop accepting applications.",
    )
    closing_date = models.DateField(
        blank=True, null=True,
        help_text="Optional. After this date the role stops accepting applications on its own.",
    )
    posted_date = models.DateField(default=timezone.localdate)

    class Meta:
        ordering = ["-posted_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("careers:detail", kwargs={"slug": self.slug})

    @property
    def requirement_list(self):
        """requirements is free text, one per line — split for <li> rendering."""
        return [line.strip() for line in self.requirements.splitlines() if line.strip()]

    @property
    def accepts_applications(self):
        """A role accepts applications while open AND not past its closing date."""
        if not self.is_open:
            return False
        if self.closing_date and self.closing_date < timezone.localdate():
            return False
        return True


class JobApplication(TimeStampedModel):
    """
    Field set follows what an engineering consultancy actually screens on:
    CV, right to work, notice period, experience. Salary expectation is
    optional on purpose — making it mandatory suppresses applications and
    is illegal to demand as salary *history* in a growing number of
    jurisdictions.
    """

    STATUS_CHOICES = [
        ("new", "New"),
        ("reviewing", "Reviewing"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        ("hired", "Hired"),
    ]

    position = models.ForeignKey(
        JobOpening, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="applications",
        help_text="Blank means a speculative application with no specific role.",
    )
    # SET_NULL above preserves the application if the role is deleted, but
    # loses which role it was for — so keep an independent text copy.
    position_title = models.CharField(
        max_length=150, blank=True,
        help_text="Snapshot of the role title at submission time.",
    )

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    location = models.CharField(max_length=120, blank=True, help_text="City / country of residence.")

    years_experience = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text="Total years of relevant professional experience."
    )
    current_employer = models.CharField(max_length=150, blank=True)
    notice_period = models.CharField(
        max_length=60, blank=True, help_text='e.g. "Immediate", "1 month"'
    )
    expected_salary = models.CharField(max_length=80, blank=True)

    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True, help_text="Portfolio, personal site, or GitHub.")

    cv_file = models.FileField(
        upload_to="careers/cv/%Y/%m/", validators=DOCUMENT_VALIDATORS,
        help_text="PDF, DOC or DOCX, max 10 MB.",
    )
    cover_letter_file = models.FileField(
        upload_to="careers/cover/%Y/%m/", blank=True, null=True,
        validators=DOCUMENT_VALIDATORS,
    )
    cover_note = models.TextField(
        blank=True, max_length=2000,
        help_text="Typed alternative to attaching a cover letter.",
    )

    heard_about = models.CharField(max_length=120, blank=True, help_text="How they found the role.")
    consent = models.BooleanField(
        default=False,
        help_text="Applicant agreed to their data being stored for recruitment purposes.",
    )

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="new")
    notes = models.TextField(blank=True, help_text="Internal notes — never shown to the applicant.")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} — {self.position_title or 'General application'}"

    def save(self, *args, **kwargs):
        if self.position and not self.position_title:
            self.position_title = self.position.title
        super().save(*args, **kwargs)
