from rest_framework import generics, filters
from django.db.models import Q
from .models import Occurrence
from .serializers import OccurrenceSerializer
from .filters import OccurrenceFilter
from rest_framework import viewsets
from .models import OccurrencePhoto
from .serializers import OccurrencePhotoSerializer

class OccurrenceListView(generics.ListCreateAPIView):
    queryset = Occurrence.objects.all().order_by("-occurred_at")
    serializer_class = OccurrenceSerializer
    filterset_class = OccurrenceFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # DRF SearchFilter uses ?search=
    search_fields = ["title", "description", "location", "category"] 
    ordering_fields = ["occurred_at", "created_at", "location", "category"]

    # custom 'q' param fallback (multi-field) for both ?q= and ?search=
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(location__icontains=q) |
                Q(category__icontains=q)
            )
        return qs

class OccurrenceViewSet(viewsets.ModelViewSet):
    queryset = Occurrence.objects.all().order_by("-occurred_at")
    serializer_class = OccurrenceSerializer

class OccurrencePhotoViewSet(viewsets.ModelViewSet):
    queryset = OccurrencePhoto.objects.all()
    serializer_class = OccurrencePhotoSerializer