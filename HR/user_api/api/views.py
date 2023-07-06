from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from user_api.models import AppUser
from django.contrib.auth.hashers import make_password


from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer,UserSerializerForPost
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password


from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		clean_data = custom_validation(request.data)
		print(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			print(clean_data)
			user = serializer.create(clean_data)
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)



class UserView(generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    ##permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return AppUser.objects.filter(role="Normal Employee")

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
