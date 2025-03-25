# services/serializers.py
from rest_framework import serializers
from .models import Service, ServiceCategory
from users.serializers import UserSerializer


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description']


class ServiceSerializer(serializers.ModelSerializer):
    # Make category accept ID for creation
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(),
        source='category',
        write_only=True
    )

    # Read-only nested serializers for response
    provider = UserSerializer(read_only=True)
    category = ServiceCategorySerializer(read_only=True)

    class Meta:
        model = Service
        fields = [
            'id',
            'provider',
            'category_id',  # Write-only field for input
            'category',  # Read-only field for output
            'name',
            'description',
            'price',
            'availability_type',
            'is_active'
        ]

    def create(self, validated_data):
        """
        Custom create method to handle provider assignment
        """
        # Remove category from validated data (it's now source='category')
        request = self.context.get('request')

        # Ensure provider is set to current user
        if request and hasattr(request, 'user'):
            validated_data['provider'] = request.user

        # Create service
        service = Service.objects.create(**validated_data)
        return service
