from django.db import models
from django.urls import reverse

from apps.core.models import OrderedModel, SEOFields, TimeStampedModel
from apps.services.models import ServiceCategory


class Project(OrderedModel, TimeStampedModel, SEOFields):
    """
    No rows are seeded for this model anywhere in this project. ConsultX
    has no completed projects under its own name yet (PROJECT_BRIEF.md
    §5/§9) — inventing case studies here would misrepresent the firm's
    track record to exactly the audience (government agencies, funding
    bodies) least able to safely take a stated history at face value.
    The frontend pass will build a genuine empty state for this section
    rather than leaving it silently blank.
    """

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    client_name = models.CharField(
        max_length=120, blank=True,
        help_text="Leave blank and mark confidential below if the client can't be named.",
    )
    is_confidential = models.BooleanField(default=False)
    location = models.CharField(max_length=120, blank=True)
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="projects",
    )
    role = models.CharField(
        max_length=200, blank=True,
        help_text='ConsultX\'s precise role, e.g. "Structural design & site supervision."',
    )
    scope = models.TextField(blank=True, help_text="Services and project stage delivered.")
    date_completed = models.DateField(blank=True, null=True)

    challenge = models.TextField(blank=True, help_text="The risk, constraint, or decision solved.")
    response = models.TextField(blank=True, help_text="The method, coordination, or control applied.")
    outcome = models.TextField(
        blank=True,
        help_text="Verified result only — no invented figures, rankings, or percentages "
                   "(see credibility guardrail in the Company Profile Strategy source).",
    )

    cover_image = models.ImageField(upload_to="projects/", blank=True, null=True)
    is_published = models.BooleanField(
        default=False,
        help_text="Off by default — publishing a project is a deliberate action, "
                   "not something that happens by saving a draft.",
    )

    class Meta:
        ordering = ["order", "-date_completed"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"slug": self.slug})


class ProjectImage(OrderedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.project.title} — image {self.order}"
