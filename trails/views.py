from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Trail
from .serializers.common import TrailSerializer



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