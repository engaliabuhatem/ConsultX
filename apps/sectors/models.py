from django.db import models
from django.urls import reverse

from apps.core.models import OrderedModel, SEOFields, TimeStampedModel


class Sector(OrderedModel, TimeStampedModel, SEOFields):
    """
    An industry ConsultX works in (water, transport, energy, buildings...).

    Not seeded. The source files never state a definitive sector list, and
    the sectors a consultancy claims are a positioning decision — listing
    one the firm has no delivery record in is the same credibility problem
    the Project model documents. Entered through the admin.

    Distinct from ServiceCategory: a service is *what* is delivered
    (structural design), a sector is *where* it is delivered (healthcare).
    The same service appears across many sectors.
    """

    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=90, unique=True)
    short_description = models.CharField(
        max_length=200, help_text="Shown on the sectors grid card."
    )
    description = models.TextField(blank=True, help_text="Full sector page copy.")
    icon = models.CharField(
        max_length=60, blank=True,
        help_text="Icon identifier used by the frontend icon set.",
    )
    image = models.ImageField(upload_to="sectors/", blank=True, null=True)
    related_services = models.ManyToManyField(
        "services.Service", blank=True, related_name="sectors",
        help_text="Services offered into this sector — shown on the sector page.",
    )
    is_featured = models.BooleanField(
        default=False, help_text="Featured sectors appear in the homepage preview grid."
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("sectors:detail", kwargs={"slug": self.slug})
