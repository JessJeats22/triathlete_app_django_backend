from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Trail



# URL: /trails (handler methods!)
class TrailShowView(APIView):
        
        
    def get(self, reqeust):
        trails = Trail.objects.all()
        print(trails)
        return Response({'detail': 'HIT TRAIL INDEX ROUTE'})