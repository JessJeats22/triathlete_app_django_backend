from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import PointOfInterest
from trails.models import Trail
from .serializers.common import POISerializer
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from utils.permissions import IsOwnerOrReadOnly
from .serializers.populated import PopulatedPOISerializer
from rest_framework.exceptions import PermissionDenied


# URL: /trails/:id/pois/
class POIListCreateView(ListCreateAPIView):
    serializer_class = POISerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return PointOfInterest.objects.filter(
        trail_id=self.kwargs['trail_id']
        )
    


    def perform_create(self, serializer):
        trail = get_object_or_404(
        Trail,
        pk=self.kwargs['trail_id']
    )

  
        if trail.created_by != self.request.user:
            raise PermissionDenied("Only the trail owner can add points of interest.")

        serializer.save(
        trail=trail,
        created_by=self.request.user
    )


# URL /pois/:id/
class POIDetailView(RetrieveUpdateDestroyAPIView):
    queryset = PointOfInterest.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PopulatedPOISerializer
        return POISerializer

