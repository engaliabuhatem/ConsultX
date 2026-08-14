from django.db import models


class TimeStampedModel(models.Model):
    """created_at/updated_at pair shared by nearly every content model."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OrderedModel(models.Model):
    """Manual display order, editable via drag-and-drop in the admin."""

    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ["order"]


class SEOFields(models.Model):
    """Per-page SEO — every page-like model gets these without repeating them."""

    meta_title = models.CharField(
        max_length=70, blank=True,
        help_text="Defaults to the page title if left blank. Keep under 60 characters.",
    )
    meta_description = models.CharField(
        max_length=160, blank=True,
        help_text="Shown in search results. Keep under 155 characters.",
    )
    og_image = models.ImageField(upload_to="seo/", blank=True, null=True)
    canonical_url = models.URLField(blank=True)

    class Meta:
        abstract = True
