from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = '__all__'
	def create(self, clean_data):
		user_obj = UserModel.objects.create_user(email=clean_data['email'], password=clean_data['password'])
		user_obj.username = clean_data['username']
		user_obj.save()
		return user_obj

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			raise ValidationError('user not found')
		return user

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = UserModel
        fields = ('email', 'username', 'role')
	

class UserSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'username')

    def get_fields(self):
        fields = super().get_fields()
        fields.pop('password', None)
        fields.pop('role', None)
        return fields

    def create(self, validated_data):
        password = "static_password"
        user = UserModel(**validated_data)
        user.set_password(password)
        user.role = "Normal Employee"
        user.save()
        return user
