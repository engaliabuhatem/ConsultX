from django.db import models

from apps.services.models import Service


class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    company = models.CharField(max_length=120, blank=True)
    service_interest = models.ForeignKey(
        Service, on_delete=models.SET_NULL, null=True, blank=True, related_name="inquiries"
    )
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Contact submission"

    def __str__(self):
        return f"{self.name} — {self.submitted_at:%Y-%m-%d}"
