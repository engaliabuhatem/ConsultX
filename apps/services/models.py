from django.db import models
from django.urls import reverse

from apps.core.models import OrderedModel, SEOFields, TimeStampedModel


class ServiceCategory(OrderedModel):
    """
    Deliberately not pre-seeded with data. Two different category schemes
    appear across the source files (the wireframe's filter tabs vs. the
    Company Profile Strategy's five-group narrative structure) — see
    PROJECT_BRIEF.md §2/§9. Whichever is chosen gets entered here through
    the admin, not hardcoded into a migration.
    """

    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=90, unique=True)

    class Meta:
        verbose_name_plural = "Service categories"
        ordering = ["order"]

    def __str__(self):
        return self.name


class Service(OrderedModel, TimeStampedModel, SEOFields):
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.PROTECT, related_name="services"
    )
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    short_description = models.CharField(
        max_length=200, help_text="Shown on the services grid card."
    )
    description = models.TextField(help_text="Full service page copy.")
    icon = models.CharField(
        max_length=60, blank=True,
        help_text="Icon identifier used by the frontend icon set (added in the frontend pass).",
    )
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    is_featured = models.BooleanField(
        default=False, help_text="Featured services appear in the homepage preview grid."
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("services:detail", kwargs={"slug": self.slug})


class ServiceFeature(OrderedModel):
    """One checklist row on a service detail page's "Key Features" block."""

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="features")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.service.title} — {self.title}"
