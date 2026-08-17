from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from auth_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    Validates and creates a new user account with profile.
    """
    fullname = serializers.CharField()
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        """Validate password matching and email uniqueness."""
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError(
                {'password': 'Passwords must match.'}
            )

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {'email': 'Email is already in use.'}
            )

        return attrs

    def create(self, validated_data):
        """Create new user and associated profile."""
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        UserProfile.objects.create(
            user=user,
            fullname=validated_data['fullname']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    
    Validates email and password credentials.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Authenticate user with provided credentials."""
        email = attrs['email']
        password = attrs['password']

        user = authenticate(
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                {'detail': 'Invalid email or password.'}
            )

        attrs['user'] = user
        return attrs