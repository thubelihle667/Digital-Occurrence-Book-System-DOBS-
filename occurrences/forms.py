from django import forms
from .models import Occurrence, OccurrencePhoto

class OccurrenceForm(forms.ModelForm):
    class Meta:
        model = Occurrence
        fields = ['title', 'description', 'category', 'location', 'occurrence_time', 'status']
        widgets = {
            'occurrence_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class OccurrencePhotoForm(forms.ModelForm):
    class Meta:
        model = OccurrencePhoto
        fields = ['image', 'caption', 'occurrence']
