from rest_framework.serializers import ModelSerializer
from ..models import PointOfInterest

class POISerializer(ModelSerializer):
    class Meta:
        model = PointOfInterest
        fields = '__all__'
        read_only_fields = ('created_by', 'trail')


