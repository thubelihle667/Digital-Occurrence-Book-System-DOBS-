from django.db import models
from django.conf import settings
from occurrences.models import Occurrence


class Report(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    summary = models.TextField(blank=True, null=True)
