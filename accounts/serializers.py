from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password', 'confirm_password')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user
    
class CustomTokenObtainPairSerialzer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        return data

