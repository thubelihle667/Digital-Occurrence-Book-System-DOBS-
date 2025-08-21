from rest_framework_nested import routers
from .views import OccurrenceViewSet, OccurrencePhotoViewSet

router = routers.SimpleRouter()
router.register(r'occurrences', OccurrenceViewSet, basename='occurrence')
router.register(r'photos', OccurrencePhotoViewSet, basename='occurrence-photo')

urlpatterns = router.urls
