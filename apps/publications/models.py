from django.db import models
from django.urls import reverse

from apps.core.models import SEOFields, TimeStampedModel
from apps.team.models import TeamMember


class Publication(TimeStampedModel, SEOFields):
    """
    A formal, downloadable document: whitepaper, technical report, case
    study, standard.

    Overlaps deliberately with blog.Post, which already has a "whitepaper"
    content_type and a whitepaper_file. The split is document-first vs.
    article-first: a Post is body copy that may carry an attachment, a
    Publication *is* the attachment and the page exists to describe and
    hand over the file. Keep long-form written pieces in Insights; put
    anything whose real payload is the PDF here.
    """

    CATEGORY_CHOICES = [
        ("whitepaper", "Whitepaper"),
        ("technical_report", "Technical Report"),
        ("case_study", "Case Study"),
        ("standard", "Standard / Guideline"),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="whitepaper")
    abstract = models.TextField(
        max_length=600, help_text="Summary shown on the card and above the download button."
    )
    pdf_file = models.FileField(
        upload_to="publications/",
        help_text="The document itself. Required — a publication with no file is just a post.",
    )
    cover_image = models.ImageField(upload_to="publications/covers/", blank=True, null=True)
    authors = models.ManyToManyField(
        TeamMember, blank=True, related_name="publications",
        help_text="Leave empty for a firm-authored document with no named author.",
    )
    published_date = models.DateField()
    is_published = models.BooleanField(
        default=False,
        help_text="Off by default — publishing is a deliberate action, not a side effect of saving.",
    )

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("publications:detail", kwargs={"slug": self.slug})

    @property
    def file_extension(self):
        """Upper-case extension ("PDF") for the download button label."""
        name = self.pdf_file.name if self.pdf_file else ""
        return name.rsplit(".", 1)[-1].upper() if "." in name else ""
