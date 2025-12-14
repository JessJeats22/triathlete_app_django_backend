from rest_framework.serializers import ModelSerializer, SerializerMethodField
from ..models import Trail

class TrailSerializer(ModelSerializer):
    is_favourited = SerializerMethodField()

    class Meta:
        model = Trail
        fields = '__all__'

    def get_is_favourited(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        return request.user.favourited_trails.filter(pk=obj.pk).exists()
