import uuid
from django.db import models
from django.conf import settings
from accounts.models import Affiliate


class Document(models.Model):
    CATEGORY_CHOICES = [
        ('policy', 'Policy'),
        ('report', 'Report'),
        ('training', 'Training'),
        ('finance', 'Finance'),
        ('hr', 'HR'),
        ('communications', 'Communications'),
        ('projects', 'Projects'),
        ('other', 'Other'),
    ]

    ACCESS_CHOICES = [
        ('global', 'All Staff'),
        ('affiliate', 'Affiliate Only'),
        ('admin', 'Admin Only'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/%Y/%m/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents'
    )
    affiliate = models.ForeignKey(
        Affiliate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents'
    )
    access_level = models.CharField(max_length=20, choices=ACCESS_CHOICES, default='global')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    def filename(self):
        import os
        return os.path.basename(self.file.name)

    def file_extension(self):
        import os
        _, ext = os.path.splitext(self.file.name)
        return ext.lower().lstrip('.')
