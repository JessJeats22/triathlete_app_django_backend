from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Trail
from .serializers.common import TrailSerializer
from rest_framework.exceptions import NotFound



# URL: /trails (handler methods!)
class TrailShowView(APIView):
        
        
    # INDEX ROUTE
    def get(self, reqeust):
        trails = Trail.objects.all()
        serializer = TrailSerializer(trails, many=True)
        return Response(serializer.data)
    
     # POST ROUTE
    def post(self, request):
        serializer = TrailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, 201)
    

# URL: /trails/:pk/
class TrailDetailView(APIView):
    
     # SHOW Route
    def get(self, request, pk):

        try:
            trail = Trail.objects.get(pk=pk)
        except Trail.DoesNotExist as e:
            raise NotFound('TRAIL NOT FOUND')

    
        serializer = TrailSerializer(trail)
        return Response(serializer.data)
    
    # PUT Route
    def put(self, request, pk):
        
        try:
            trail = Trail.objects.get(pk=pk)
        except Trail.DoesNotExist:
            raise NotFound('Trail not found')
            
        serializer = TrailSerializer(instance=trail, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    # DELETE Route
    def delete(self, request, pk):
        pass