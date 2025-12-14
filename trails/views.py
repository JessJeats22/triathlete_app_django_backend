from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Trail
from .serializers.common import TrailSerializer
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404




# URL: /trails (handler methods!)
class TrailShowView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
        
    # INDEX ROUTE
    def get(self, request):
        trails = Trail.objects.all()
        serializer = TrailSerializer(trails, many=True, context={'request': request})
        return Response(serializer.data)
    
     # POST ROUTE
    def post(self, request):
        request.data['created_by'] = request.user.id
        serializer = TrailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, 201)
    

# URL: /trails/:pk/
class TrailDetailView(APIView):

    permission_classes = [IsOwnerOrReadOnly]

    # Get Trail Object
    def get_trail(self, pk):
        try:
            return Trail.objects.get(pk=pk)
        except Trail.DoesNotExist:
            raise NotFound('Trail not found')
    
     # SHOW Route
    def get(self, request, pk):
        trail = self.get_trail(pk)
        serializer = TrailSerializer(trail, context={'request': request})
        return Response(serializer.data)
    
    # PUT Route
    def put(self, request, pk):
        trail = self.get_trail(pk)
        self.check_object_permissions(request, trail)    
        serializer = TrailSerializer(instance=trail, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

    # PATCH Route
    def patch(self, request, pk):
        trail = self.get_trail(pk)
        self.check_object_permissions(request, trail)
        serializer = TrailSerializer(instance=trail, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



    # DELETE Route
    def delete(self, request, pk):
        trail = self.get_trail(pk)
        self.check_object_permissions(request, trail)
        trail.delete()
        return Response(status=204)
    

class TrailFavouriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        trail = get_object_or_404(Trail, pk=pk)
        request.user.favourited_trails.add(trail)
        return Response({'detail': 'Trail favourited'}, status=201)
    
    def delete(self, request, pk):
        trail = get_object_or_404(Trail, pk=pk)
        request.user.favourited_trails.remove(trail)
        return Response(status=204)
