# services/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Service, ServiceCategory
from .serializers import ServiceSerializer, ServiceCategorySerializer


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def create(self, request, *args, **kwargs):
        """
        Enhanced service creation with detailed error handling
        """
        try:
            # Validate category exists
            category_id = request.data.get('category_id')
            if not category_id:
                return Response({
                    'error': 'Category ID is required',
                    'available_categories': list(
                        ServiceCategory.objects.values('id', 'name')
                    )
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Verify category exists
                ServiceCategory.objects.get(id=category_id)
            except ServiceCategory.DoesNotExist:
                return Response({
                    'error': f'Category with ID {category_id} does not exist',
                    'available_categories': list(
                        ServiceCategory.objects.values('id', 'name')
                    )
                }, status=status.HTTP_404_NOT_FOUND)

            # Proceed with standard creation
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Save service with current user as provider
            service = serializer.save(provider=request.user)

            return Response(
                self.get_serializer(service).data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response({
                'error': 'Unexpected error during service creation',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
