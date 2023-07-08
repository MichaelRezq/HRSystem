from tokenize import TokenError
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignUpSerializer
from .tokens import create_jwt_pair_for_user
from django.contrib.auth.hashers import make_password
from .serializers import  UserSerializer,UserSerializerForPost
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
# Create your views here.


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {"message": "User Created Successfully", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:

            tokens = create_jwt_pair_for_user(user)

            response = {"message": "Login Successfull", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password"})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(data={"message": "Logout Successful"}, status=status.HTTP_200_OK)
            except TokenError:
                return Response(data={"message": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"message": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

class UserView(generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return User.objects.filter(role="Normal Employee")

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT' :
            return UserSerializerForPost
        else:
            return UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        static_password = "static_password"
        mutable_data = request.data.copy()  # Create a mutable copy of the QueryDict
        mutable_data["password"] = make_password(static_password)
        mutable_data["role"] = "Normal Employee"
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)
        if user:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# Retrieve, update or delete a employee instance
class UserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = UserSerializerForPost

