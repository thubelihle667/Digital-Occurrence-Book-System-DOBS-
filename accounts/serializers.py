from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confrim_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password', 'confirm_password')

        def validate(self, data):
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError('Passwords do not match')
            return data 
        
        def create(self,validated_data):
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                role=validated_data['role'],
                password=validated_data['password']
            )
            return user
        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)