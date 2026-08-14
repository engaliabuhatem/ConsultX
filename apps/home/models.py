from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import OrderedModel, TimeStampedModel


class HomeHero(TimeStampedModel):
    """Singleton — hero section content. Section order on the page is
    hardcoded in the template (see wireframe notes: layout structure is
    fine to hardcode, the *content within* it is not)."""

    headline = models.CharField(max_length=150)
    subheadline = models.CharField(max_length=250, blank=True)
    background_image = models.ImageField(upload_to="home/")
    cta_label = models.CharField(max_length=40, default="Start Your Project")
    cta_url = models.CharField(max_length=200, default="/contact/")

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def clean(self):
        if not self.pk and HomeHero.objects.exists():
            raise ValidationError("Hero Section already exists — edit the existing entry.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return "Hero Section"


class StatCounter(OrderedModel):
    """"150+ Projects Completed" style stat, editable and reorderable."""

    value = models.CharField(max_length=20, help_text='e.g. "150+", "25+"')
    label = models.CharField(max_length=60, help_text='e.g. "Projects Completed"')

    def __str__(self):
        return f"{self.value} {self.label}"


class CTABanner(TimeStampedModel):
    """Singleton — the full-width call-to-action banner."""

    headline = models.CharField(max_length=150, default="Ready to start your project?")
    subtext = models.CharField(max_length=250, blank=True)
    button_label = models.CharField(max_length=40, default="Contact Us")
    button_url = models.CharField(max_length=200, default="/contact/")

    class Meta:
        verbose_name = "CTA Banner"
        verbose_name_plural = "CTA Banner"

    def clean(self):
        if not self.pk and CTABanner.objects.exists():
            raise ValidationError("CTA Banner already exists — edit the existing entry.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return "CTA Banner"
