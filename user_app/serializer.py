from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

UserModel = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)

    class Meta:
        model = UserModel
        fields = ["email", "password", "first_name"]

    def create(self, validated_data):
        user_obj = UserModel.objects.create_user(email=validated_data['email'],
                                                 password=validated_data['password'])
        user_obj.first_name = validated_data['first_name']
        user_obj.save()
        return user_obj

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = UserModel
        exclude = []
    def check_user(self, clean_data):
        user = authenticate(email=clean_data['email'], password=clean_data['password'])
        if not user:
            raise ValidationError("user not found")
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("email", "first_name")
