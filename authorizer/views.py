from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from . import serializers
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken,BlacklistedToken

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegisterSerializer

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Validate and blacklist the refresh token
            token = RefreshToken(refresh_token)
            try:
                outstanding_token = OutstandingToken.objects.get(token=token)
            except OutstandingToken.DoesNotExist:
                return Response({'detail': 'Token not found.'}, status=status.HTTP_400_BAD_REQUEST)
            BlacklistedToken.objects.create(token=outstanding_token)

            return Response(status=status.HTTP_200_OK)
        except TokenError as e:
            # TokenError handles cases where the token is invalid or already blacklisted
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # General exception handling for other possible issues
            return Response({'detail': 'An error occurred: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)