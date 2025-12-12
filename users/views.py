from .serializers.common import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Path: /auth/sign-up/
class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({ 'message': 'Registration successful' }, 201)