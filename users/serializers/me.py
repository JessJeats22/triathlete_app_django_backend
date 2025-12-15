from rest_framework.serializers import ModelSerializer
from ..models import User
from trails.serializers.summary import TrailSummarySerializer

class MeSerializer(ModelSerializer):
    created_trails = TrailSummarySerializer(
        many=True,
        read_only=True,
        source='trails_owned'
    )

    favourited_trails = TrailSummarySerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile_image', 'created_trails', 'favourited_trails')