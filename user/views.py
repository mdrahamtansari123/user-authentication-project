from django.shortcuts import render
from .serializers import  Market_UserSerializer
from .models import Market_User
from rest_framework import generics, status
from rest_framework import viewsets,permissions,parsers
from rest_framework import permissions

from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
# Create your views here.
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperUser, IsAdminUser, IsRegularUser
from rest_framework.exceptions import AuthenticationFailed
from .authentication import CustomAuthentication

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    parser_classes = [parsers.FormParser,parsers.MultiPartParser]
    serializer_class = RegisterSerializer
    permission_classes = [IsSuperUser | IsAdminUser | IsRegularUser]
    authentication_classes = [CustomAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "mobile_number": user.mobile_number,
                "address": user.address,
                "user_type": user.user_type,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            }
        }, status=status.HTTP_201_CREATED)


    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    parser_classes = [parsers.FormParser,parsers.MultiPartParser]
    # permission_classes = []
    # authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "mobile_number": user.mobile_number,
                "address": user.address,
                "user_type": user.user_type,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
    # @permission_classes([TokenAuthentication])
    # @permission_classes([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return Response({
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "mobile_number": user.mobile_number,
                    "address": user.address,
                    "user_type": user.user_type,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                }
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    
class AdminView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [] 
    parser_classes = [parsers.FormParser,parsers.MultiPartParser]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise AuthenticationFailed('Not authenticated')  
        if user.user_type in ['superuser', 'admin']:
            return User.objects.all()
        
        return User.objects.filter(user_type__in=['admin', 'user'])

from rest_framework.views import APIView
class CheckUserRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            "username": user.username,
            "user_type": user.user_type,
        })


class Market_UserViewSet(viewsets.ModelViewSet):
    queryset = Market_User.objects.all()
    serializer_class = Market_UserSerializer
    parser_classes = [parsers.FormParser,parsers.MultiPartParser]
    delete_response = {"status": "success", "message": "standard deleted"}
    update_response = {"status": "success", "message": "standard updated"}
    get_response = {"status": "success", "message": ""}
    create_response = {"status": "success", "message": "standard created"}