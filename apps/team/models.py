from django.db import models

from apps.core.models import OrderedModel, TimeStampedModel


class TeamMember(OrderedModel, TimeStampedModel):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, help_text='e.g. "Principal Engineer, Founder"')
    bio = models.TextField(blank=True)
    credentials = models.CharField(
        max_length=200, blank=True,
        help_text='e.g. "PE, Egyptian Engineers Syndicate" — only verified credentials.',
    )
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    linkedin_url = models.URLField(blank=True)
    is_founder = models.BooleanField(default=False)
    is_leadership = models.BooleanField(
        default=False,
        help_text="Shown on the Leadership page. Kept separate from 'is founder' "
                  "because a firm's leadership and its founders are not the same set — "
                  "a hired managing director is one but not the other.",
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name
