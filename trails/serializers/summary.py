from rest_framework.serializers import ModelSerializer
from ..models import Trail

class TrailSummarySerializer(ModelSerializer):
    class Meta:
        model = Trail
        fields = ('id', 'name', 'trail_type')