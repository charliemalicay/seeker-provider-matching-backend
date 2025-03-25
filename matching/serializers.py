# matching/serializers.py
from rest_framework import serializers
from matching.models import MatchRequest

from users.serializers import UserSerializer
from services.serializers import ServiceSerializer

from users.models import User
from services.models import Service


class MatchRequestSerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type='provider'),
        required=True
    )
    service = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        required=True
    )

    class Meta:
        model = MatchRequest
        fields = [
            'id',
            'seeker',
            'provider',
            'service',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'seeker', 'status', 'created_at', 'updated_at']

    def validate(self, attrs):
        """
        Comprehensive validation method
        """
        # Get request from context
        request = self.context.get('request')

        # Ensure request exists and user is authenticated
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError({
                'detail': 'Authentication required'
            })

        # Validate user is a seeker
        # if request.user.user_type != 'seeker':
        #     raise serializers.ValidationError({
        #         'seeker': 'Only service seekers can create match requests'
        #     })

        # Validate provider
        provider = attrs.get('provider')
        if not provider or provider.user_type != 'provider':
            raise serializers.ValidationError({
                'provider': 'Invalid provider selected'
            })

        # Validate service
        service = attrs.get('service')
        if not service:
            raise serializers.ValidationError({
                'service': 'Service is required'
            })

        # Ensure service belongs to the selected provider
        if service.provider != provider:
            raise serializers.ValidationError({
                'service': 'Selected service does not belong to the chosen provider'
            })

        # Check for existing pending requests
        existing_request = MatchRequest.objects.filter(
            seeker=request.user,
            provider=provider,
            service=service,
            status='pending'
        ).exists()

        if existing_request:
            raise serializers.ValidationError({
                'detail': 'A pending request for this service already exists'
            })

        return attrs

    def create(self, validated_data):
        """
        Override create method to set seeker automatically
        """
        # Get the current user (seeker) from request context
        request = self.context.get('request')

        # Ensure seeker is set to current user
        validated_data['seeker'] = request.user

        # Set default status
        validated_data['status'] = 'pending'

        # Create match request
        return super().create(validated_data)
