from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from cookie_token.auth_class import CookieJWTAuthentication
from cookie_token.serializers import CookieTokenRefreshSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import ModelSerializer


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 31  # 31 days
            response.set_cookie(
                'refresh_token',
                response.data['refresh'],
                max_age=cookie_max_age,
                httponly=True,
                secure=True,
                samesite='None'
            )
            del response.data['refresh']

        if response.data.get('access'):
            access_token_expiry = 3600 # 1 hour
            response.set_cookie(
                'access_token',
                response.data['access'],
                max_age=access_token_expiry,
                httponly=True,
                secure=True,
                samesite='None'
            )
            del response.data['access']

        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 31  # 31 days
            response.set_cookie(
                'refresh_token',
                response.data['refresh'],
                max_age=cookie_max_age,
                httponly=True,
                secure=True,
                samesite='None'
            )
            del response.data['refresh']

        if response.data.get('access'):
            access_token_expiry = 3600  # 1 hour
            response.set_cookie(
                'access_token',
                response.data['access'],
                max_age=access_token_expiry,
                httponly=True,
                secure=True,
                samesite='None'
            )
            del response.data['access']

        return super().finalize_response(request, response, *args, **kwargs)

    serializer_class = CookieTokenRefreshSerializer


class CookieTokenLogoutView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        response = Response(status=204)
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        return response


class CookieTokenObtainCurrentUserView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })


class RegisterSerializer(ModelSerializer):

    class Meta:

        model = User

        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False, 'default': ''},
            'last_name': {'required': False, 'default': ''},
            'username': {'required': False, 'default': ''}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)