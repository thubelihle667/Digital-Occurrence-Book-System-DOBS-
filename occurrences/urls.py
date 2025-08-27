from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OccurrenceViewSet, OccurrencePhotoViewSet, OccurrenceListView

# router creation and viewsets registration
router = DefaultRouter()
router.register(r'occurrences', OccurrenceViewSet, basename='occurrence')
router.register(r'photos', OccurrencePhotoViewSet, basename='occurrence-photo')

urlpatterns = [
    path("", include(router.urls)),  # include all router URLs
    path("list/", OccurrenceListView.as_view(), name="occurrence-list"),  # extra list view
]
