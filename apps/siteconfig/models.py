from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from apps.core.models import SEOFields, TimeStampedModel

hex_color_validator = RegexValidator(
    regex=r"^#[0-9A-Fa-f]{6}$",
    message="Enter a 6-digit hex color, e.g. #d6481f (including the #).",
)


class SiteSettings(TimeStampedModel, SEOFields):
    """
    Singleton: one row, holds everything global (logo, contact, socials,
    footer, default SEO). Enforced via clean() rather than a hardcoded
    fixture, so the admin panel remains the single source of truth.
    """

    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    favicon = models.ImageField(upload_to="site/", blank=True, null=True)
    accent_color = models.CharField(
        max_length=7, blank=True, validators=[hex_color_validator],
        help_text="Hex color, e.g. #d6481f (include the #). Overrides the site's accent "
                   "color everywhere it's used — buttons, links, highlights — without "
                   "needing a code change. Leave blank to use the built-in default.",
    )

    # Real values are placeholders until the company supplies them —
    # see PROJECT_BRIEF.md §8/§9. Left blank rather than filled with
    # invented-but-plausible data.
    contact_phone = models.CharField(max_length=40, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_address = models.TextField(blank=True)

    linkedin_url = models.URLField(blank=True)
    x_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    footer_text = models.CharField(
        max_length=200,
        default="All rights reserved.",
        help_text='Appears after "© {year} {company name}." in the footer.',
    )
    professional_indemnity_notice = models.CharField(
        max_length=200, blank=True,
        help_text="Optional PI insurance verification line for the footer "
                   "(requested in the launch-readiness report).",
    )

    default_meta_title = models.CharField(max_length=70, blank=True)
    default_meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def clean(self):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError("Site Settings already exists — edit the existing entry.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return "Site Settings"

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
