from django.db import models
from django.urls import reverse

from apps.core.models import SEOFields, TimeStampedModel
from apps.team.models import TeamMember


class InsightCategory(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=90, unique=True)

    class Meta:
        verbose_name_plural = "Insight categories"

    def __str__(self):
        return self.name


class Post(TimeStampedModel, SEOFields):
    CONTENT_TYPE_CHOICES = [
        ("article", "Technical Article"),
        ("whitepaper", "Whitepaper"),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    category = models.ForeignKey(
        InsightCategory, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    content_type = models.CharField(max_length=12, choices=CONTENT_TYPE_CHOICES, default="article")
    excerpt = models.CharField(max_length=250)
    content = models.TextField()
    whitepaper_file = models.FileField(
        upload_to="insights/whitepapers/", blank=True, null=True,
        help_text="PDF download — used when content_type is Whitepaper.",
    )
    featured_image = models.ImageField(upload_to="insights/", blank=True, null=True)
    author = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, related_name="posts")
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})
