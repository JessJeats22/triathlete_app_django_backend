from rest_framework.serializers import ModelSerializer, SerializerMethodField
from ..models import Trail

class TrailSerializer(ModelSerializer):
    is_favourited = SerializerMethodField()

    class Meta:
        model = Trail
        fields = '__all__'
        read_only_fields = (
            "id",
            "created_by",
            "images",
            "gpx_url",
            "distance_km",
            "elevation_gain_m",
            "elevation_loss_m",
            "elevation_min_m",
            "elevation_max_m",
            "is_favourited",
        )

    def get_is_favourited(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        return request.user.favourited_trails.filter(pk=obj.pk).exists()
