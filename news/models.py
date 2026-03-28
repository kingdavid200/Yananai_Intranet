import uuid
from django.db import models
from django.conf import settings
from accounts.models import Affiliate


class Announcement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    body = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='announcements'
    )
    affiliate = models.ForeignKey(
        Affiliate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='announcements',
        help_text='Leave blank for an org-wide announcement'
    )
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title

    @property
    def is_global(self):
        return self.affiliate is None
