from rest_framework.serializers import ModelSerializer
from ..models import Trail

class TrailSerializer(ModelSerializer):
    class Meta:
        model = Trail
        fields = '__all__'