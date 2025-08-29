from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Occurrence, OccurrencePhoto
from .serializers import OccurrenceSerializer, OccurrencePhotoSerializer
from .filters import OccurrenceFilter


class OccurrenceViewSet(viewsets.ModelViewSet):
    queryset = Occurrence.objects.all().order_by("-occurred_at")
    serializer_class = OccurrenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = OccurrenceFilter  
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "location", "category"]
    ordering_fields = ["occurred_at", "created_at", "location", "category"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        occurrence_id = instance.id
        self.perform_destroy(instance)
        return Response(
            {"message": f"Report with ID {occurrence_id} has been successfully deleted."},
            status=status.HTTP_200_OK
        )

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
    
class OccurrencePhotoViewSet(viewsets.ModelViewSet):
    queryset = OccurrencePhoto.objects.all().order_by("-uploaded_at")
    serializer_class = OccurrencePhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
