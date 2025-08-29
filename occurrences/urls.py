from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OccurrenceViewSet, OccurrencePhotoViewSet

router = DefaultRouter()
router.register(r'occurrences', OccurrenceViewSet, basename='occurrence')
router.register(r'occurrence-photos', OccurrencePhotoViewSet, basename='occurrencephoto')

urlpatterns = [
    path("", include(router.urls)),
]

