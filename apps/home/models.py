from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import OrderedModel, TimeStampedModel


class HomeHero(TimeStampedModel):
    """Singleton — hero section content. Section order on the page is
    hardcoded in the template (see wireframe notes: layout structure is
    fine to hardcode, the *content within* it is not)."""

    headline = models.CharField(max_length=150)
    subheadline = models.CharField(max_length=250, blank=True)
    background_image = models.ImageField(upload_to="home/", blank=True, null=True)
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


class PracticeChapter(OrderedModel, TimeStampedModel):
    """
    One full-bleed "chapter" band on the homepage — the sustainability /
    heavy-infrastructure / hydraulic sequence from the approved design comp.

    Editable rather than hardcoded for the same reason HomeHero is: the
    *layout* (photo, tint, copy anchored bottom-left) belongs to the
    template, the words and the photograph do not. The palette field picks
    which of the three practice color sets the band is drawn in, so the
    template never has to know which chapter it is rendering.

    When the table is empty the view falls back to DEFAULTS below, so a
    fresh install still shows the designed page instead of three gaps.
    """

    PALETTE_SUSTAINABILITY = "a"
    PALETTE_INFRASTRUCTURE = "b"
    PALETTE_HYDRAULIC = "c"
    PALETTE_CHOICES = [
        (PALETTE_SUSTAINABILITY, "A · Sustainability (gold / forest)"),
        (PALETTE_INFRASTRUCTURE, "B · Heavy Infrastructure (clay / grey)"),
        (PALETTE_HYDRAULIC, "C · Hydraulic Authority (teal / mint)"),
    ]

    eyebrow = models.CharField(
        max_length=60, help_text='Small label above the heading, e.g. "Direction A · Sustainability".'
    )
    title = models.CharField(max_length=120, help_text="Large heading. Keep it to a short sentence.")
    body = models.TextField(help_text="One paragraph. Roughly 200–260 characters reads best.")
    image = models.ImageField(
        upload_to="home/chapters/", blank=True, null=True,
        help_text="Full-bleed background photo. Landscape, at least 1600px wide.",
    )
    palette = models.CharField(
        max_length=1, choices=PALETTE_CHOICES, default=PALETTE_SUSTAINABILITY,
        help_text="Which practice palette this band is drawn in.",
    )
    link_url = models.CharField(
        max_length=200, blank=True, help_text='Optional. e.g. "/services/" — leave blank for no link.'
    )
    link_label = models.CharField(max_length=40, blank=True, default="Explore the practice")

    class Meta:
        ordering = ["order"]
        verbose_name = "Homepage Chapter"
        verbose_name_plural = "Homepage Chapters"

    def __str__(self):
        return self.title

    #: Stock art per palette, shipped in static/img/. Used when no photo has
    #: been uploaded yet, so a half-filled chapter still looks designed
    #: instead of falling back to a flat black band.
    DEFAULT_IMAGES = {
        PALETTE_SUSTAINABILITY: "img/chapter-sustainability.jpg",
        PALETTE_INFRASTRUCTURE: "img/chapter-infrastructure.jpg",
        PALETTE_HYDRAULIC: "img/chapter-hydraulic.jpg",
    }

    @property
    def static_image(self):
        """Path under static/ for this chapter's fallback photo. The template
        reads `image` first and only falls through to here."""
        return self.DEFAULT_IMAGES.get(self.palette)


#: Shown when no PracticeChapter rows exist. Mirrors the approved comp,
#: including the three photographs shipped in static/img/.
DEFAULT_CHAPTERS = [
    {
        "eyebrow": "Direction A · Sustainability",
        "title": "Impact through precision.",
        "body": (
            "Systems-first. Bright by design. Nothing wasted. Our sustainability practice "
            "designs infrastructure that performs today without borrowing against tomorrow."
        ),
        "palette": "a",
        "static_image": "img/chapter-sustainability.jpg",
        "link_url": "",
        "link_label": "",
    },
    {
        "eyebrow": "Direction B · Heavy Infrastructure",
        "title": "As we evolve, our execution should too.",
        "body": (
            "Complex challenges, met without the baggage of the past — the agility of a "
            "startup with the rigorous technical standards heavy infrastructure demands."
        ),
        "palette": "b",
        "static_image": "img/chapter-infrastructure.jpg",
        "link_url": "",
        "link_label": "",
    },
    {
        "eyebrow": "Direction C · Hydraulic Authority",
        "title": "From source to surface.",
        "body": (
            "Precision-engineered hydraulic systems and industrial solutions, powering the "
            "machines that move the world — from deep authority to bright clarity."
        ),
        "palette": "c",
        "static_image": "img/chapter-hydraulic.jpg",
        "link_url": "",
        "link_label": "",
    },
]
