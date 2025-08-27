from django.db import models
from django.conf import settings
from occurrences.models import Occurrence

class Report(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    # one report can summarize multiple occurrences
    occurrences = models.ManyToManyField(Occurrence, blank=True, related_name="reports")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

