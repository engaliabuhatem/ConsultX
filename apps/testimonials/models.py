from django.db import models

from apps.core.models import OrderedModel, TimeStampedModel
from apps.projects.models import Project


class Testimonial(OrderedModel, TimeStampedModel):
    quote = models.TextField()
    client_name = models.CharField(max_length=100)
    client_role = models.CharField(max_length=150, blank=True, help_text="Role and company.")
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="testimonials",
    )
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.client_name} — {self.quote[:40]}"
