from django.db import models

from apps.core.models import TimeStampedModel
from apps.core.validators import DOCUMENT_VALIDATORS


class PartnerApplication(TimeStampedModel):
    """
    Partner / supplier prequalification enquiry.

    Field set follows the standard public-sector consultant prequalification
    pattern (statement of experience, financial standing, certifications,
    insurance, disclosure) rather than a generic "company + message" form,
    because that is the information actually needed to decide whether a firm
    can be worked with.

    This is a *first-stage* enquiry, not a completed prequalification: it
    collects enough to triage, and the formal packet is requested by email
    afterwards. Anything requiring signature, notarisation, or audited
    accounts deliberately stays off a public web form.
    """

    PARTNERSHIP_TYPE_CHOICES = [
        ("subconsultant", "Sub-consultant / specialist services"),
        ("joint_venture", "Joint venture on bids"),
        ("supplier", "Supplier / vendor"),
        ("technology", "Technology or software partner"),
        ("academic", "Academic / research collaboration"),
        ("other", "Other"),
    ]
    EMPLOYEE_COUNT_CHOICES = [
        ("1-10", "1–10"),
        ("11-50", "11–50"),
        ("51-200", "51–200"),
        ("201-500", "201–500"),
        ("500+", "More than 500"),
    ]
    STATUS_CHOICES = [
        ("new", "New"),
        ("reviewing", "Reviewing"),
        ("approved", "Approved"),
        ("declined", "Declined"),
    ]

    # --- Company identity ---
    company_name = models.CharField(max_length=180)
    registration_number = models.CharField(
        max_length=80, blank=True, help_text="Commercial register / company number."
    )
    tax_id = models.CharField(max_length=80, blank=True)
    website = models.URLField(blank=True)
    country = models.CharField(max_length=80)
    city = models.CharField(max_length=80, blank=True)
    year_established = models.PositiveIntegerField(null=True, blank=True)
    employee_count = models.CharField(
        max_length=10, choices=EMPLOYEE_COUNT_CHOICES, blank=True
    )

    # --- Primary contact ---
    contact_name = models.CharField(max_length=120)
    contact_title = models.CharField(max_length=120, blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=40)

    # --- Capability ---
    partnership_type = models.CharField(max_length=20, choices=PARTNERSHIP_TYPE_CHOICES)
    sectors = models.ManyToManyField(
        "sectors.Sector", blank=True, related_name="partner_applications",
        help_text="Sectors the firm can deliver into.",
    )
    capabilities = models.TextField(
        help_text="Services, disciplines, and delivery capacity offered."
    )
    key_clients = models.TextField(
        blank=True, help_text="Reference clients or projects — only ones that may be named."
    )
    annual_turnover = models.CharField(
        max_length=80, blank=True, help_text="Approximate, with currency."
    )

    # --- Standing ---
    certifications = models.TextField(
        blank=True, help_text="ISO 9001, professional body registrations, trade licences."
    )
    has_professional_indemnity = models.BooleanField(
        default=False, verbose_name="Holds professional indemnity insurance"
    )
    has_conflict_of_interest = models.BooleanField(
        default=False,
        verbose_name="Declares a potential conflict of interest",
        help_text="Ticked means the firm has disclosed one in the notes below.",
    )
    conflict_details = models.TextField(blank=True)

    # --- Documents ---
    company_profile_file = models.FileField(
        upload_to="partners/profiles/%Y/%m/", blank=True, null=True,
        validators=DOCUMENT_VALIDATORS, help_text="PDF, DOC or DOCX, max 10 MB.",
    )
    trade_licence_file = models.FileField(
        upload_to="partners/licences/%Y/%m/", blank=True, null=True,
        validators=DOCUMENT_VALIDATORS, help_text="PDF, DOC or DOCX, max 10 MB.",
    )

    # --- Meta ---
    message = models.TextField(blank=True, help_text="Anything else about the proposed partnership.")
    consent = models.BooleanField(
        default=False, help_text="Applicant agreed to their data being stored for assessment."
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="new")
    notes = models.TextField(blank=True, help_text="Internal notes — never shown to the applicant.")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Partner application"

    def __str__(self):
        return f"{self.company_name} — {self.get_partnership_type_display()}"
