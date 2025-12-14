from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import PointOfInterest
from trails.models import Trail
from .serializers.common import POISerializer
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView




# Create your views here.

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

        serializer.save(
        owner=self.request.user,
        trail=trail
    )

# URL /pois/:id/
class POIDetailView(RetrieveUpdateDestroyAPIView):
    pass