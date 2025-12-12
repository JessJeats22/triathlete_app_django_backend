from rest_framework import serializers
from ..models import User

class UserSerializer(serializers.ModelSerializer):
   password = serializers.CharField(write_only=True)
   confirm_password = serializers.CharField(write_only=True)
   
   class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_image', 'password', 'confirm_password', 'is_staff']


