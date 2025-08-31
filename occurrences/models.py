from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
import os
from django.utils.timezone import now


def occurrence_image_upload_to(instance, filename):
    """Dynamically build upload path for occurrence images"""
    ext = filename.split('.')[-1]
    filename = f"{now().strftime('%Y%m%d%H%M%S')}.{ext}"

    # If the occurrence has a reporting user, save under their folder
    if instance.reported_by and instance.reported_by.id:
        return os.path.join("occurrences", str(instance.reported_by.id), filename)

    # Otherwise, save in unassigned folder
    return os.path.join("occurrences", "unassigned", filename)


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
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='occurrences'
    )
    occurred_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(
        upload_to=occurrence_image_upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class OccurrencePhoto(models.Model):
    occurrence = models.ForeignKey(
        Occurrence, on_delete=models.CASCADE, related_name="photos"
    )
    photo = models.ImageField(upload_to="occurrence_photos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.occurrence.title}"
