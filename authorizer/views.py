from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from . import serializers
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegisterSerializer

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)