from .common import TrailSerializer
from poi.serializers.common import POISerializer
from users.serializers.common import BasicUserSerializer

class PopulatedTrailSerializer(TrailSerializer):
    created_by = BasicUserSerializer(read_only=True)
    points_of_interest = POISerializer(
        many=True,
        read_only=True
    )