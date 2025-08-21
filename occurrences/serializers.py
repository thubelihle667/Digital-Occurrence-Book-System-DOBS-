from rest_framework import serializers
from django.utils import timezone
from django.db.models import Q
from PIL import Image
from .models import Occurrence, OccurrencePhoto

class OccurrencePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccurrencePhoto
        fields = ['id', 'image', 'caption', 'uploaded_by', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at']

    def validate_image(self, file):
        # Size limit: 5 MB
        max_mb = 5
        if file.size > max_mb * 1024 * 1024:
            raise serializers.ValidationError(f'Image too large (>{max_mb}MB).')
        # Verify it's a real image
        try:
            img = Image.open(file)
            img.verify()
        except Exception:
            raise serializers.ValidationError('Uploaded file is not a valid image.')
        return file

class OccurrencePhotoReadSerializer(serializers.ModelSerializer):
    """Use when nesting photos inside Occurrence response."""
    class Meta:
        model = OccurrencePhoto
        fields = ['id', 'image', 'caption', 'uploaded_at']

class OccurrenceSerializer(serializers.ModelSerializer):
    photos = OccurrencePhotoReadSerializer(many=True, read_only=True)

    class Meta:
        model = Occurrence
        fields = [
            'id', 'reference_no', 'title', 'description', 'category', 'location',
            'occurrence_time', 'reported_by', 'status', 'created_at', 'photos'
        ]
        read_only_fields = ['id', 'reference_no', 'reported_by', 'created_at', 'photos']

    def validate_occurrence_time(self, value):
        # Disallow future timestamps (with tiny tolerance of 5 minutes)
        now = timezone.now()
        if value > now + timezone.timedelta(minutes=5):
            raise serializers.ValidationError("Occurrence time cannot be in the future.")
        return value

    def validate(self, attrs):
        # Duplicate guard: same title + location within a 15-minute window
        title = attrs.get('title', getattr(self.instance, 'title', None))
        location = attrs.get('location', getattr(self.instance, 'location', None))
        occurrence_time = attrs.get('occurrence_time', getattr(self.instance, 'occurrence_time', None))

        if title and location and occurrence_time:
            window = timezone.timedelta(minutes=15)
            qs = Occurrence.objects.filter(
                title__iexact=title.strip(),
                location__iexact=location.strip(),
                occurrence_time__range=(occurrence_time - window, occurrence_time + window)
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("Possible duplicate: similar occurrence within 15 minutes at the same location.")
        return attrs

    def create(self, validated_data):
        validated_data['reported_by'] = self.context['request'].user
        return super().create(validated_data)
