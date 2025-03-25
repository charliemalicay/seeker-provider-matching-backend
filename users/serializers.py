# users/serializers.py
from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


# from .models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'user_type', 'location', 'phone_number']
#         extra_kwargs = {'password': {'write_only': True}}

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,  # Password won't be returned in responses
        required=True,
        validators=[validate_password]  # Django's built-in password validation
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password',
            'confirm_password', 'user_type',
            'location', 'phone_number'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'user_type': {'required': True}
        }

    def validate(self, attrs):
        """
        Password validation and confirmation
        """
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        """
        Create user with hashed password
        """
        try:
            # Create user using create_user method to properly hash password
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                user_type=validated_data.get('user_type', 'seeker'),
                location=validated_data.get('location', ''),
                phone_number=validated_data.get('phone_number', '')
            )
            return user
        except Exception as e:
            # Detailed error logging
            raise serializers.ValidationError(
                {"error": f"User creation failed: {str(e)}"}
            )
