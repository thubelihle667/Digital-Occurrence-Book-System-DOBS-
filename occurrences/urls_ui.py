from django.urls import path
from .views_ui import (
    OccurrenceListView, OccurrenceDetailView, OccurrenceCreateView,
    OccurrenceUpdateView, OccurrencePhotoCreateView
)

urlpatterns = [
    path('occurrences/', OccurrenceListView.as_view(), name='occurrence_list'),
    path('occurrences/new/', OccurrenceCreateView.as_view(), name='occurrence_create'),
    path('occurrences/<int:pk>/', OccurrenceDetailView.as_view(), name='occurrence_detail'),
    path('occurrences/<int:pk>/edit/', OccurrenceUpdateView.as_view(), name='occurrence_edit'),
    path('occurrences/photo/new/', OccurrencePhotoCreateView.as_view(), name='occurrence_photo_create'),
]
