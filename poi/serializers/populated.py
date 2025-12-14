from .common import POISerializer
from trails.serializers.common import TrailSerializer
from users.serializers.common import BasicUserSerializer

from users.serializers.common import BasicUserSerializer

class PopulatedPOISerializer(POISerializer):
    trail = TrailSerializer(read_only=True)
    owner = BasicUserSerializer(read_only=True)
