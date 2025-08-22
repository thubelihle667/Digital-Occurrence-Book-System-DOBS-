from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator


def occurrence_photo_path(instance, filename):
    return f"occurrences/{instance.id}/{filename}"


class Occurrence(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    CATEGORY_CHOICES = [
        ('theft', 'Theft'),
        ('accident', 'Accident'),
        ('fire', 'Fire'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='low')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='occurrences'
    )
    occurred_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to=occurrence_photo_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title
