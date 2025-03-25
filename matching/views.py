# matching/views.py
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from matching.models import MatchRequest
from matching.serializers import MatchRequestSerializer
from matching.services import MatchingService
from matching.utils import calculate_match_score

from services.serializers import ServiceSerializer


class MatchRequestViewSet(viewsets.ModelViewSet):
    queryset = MatchRequest.objects.all()
    serializer_class = MatchRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter queryset based on user type
        """
        user = self.request.user
        if user.user_type == 'seeker':
            return MatchRequest.objects.filter(seeker=user)
        elif user.user_type == 'provider':
            return MatchRequest.objects.filter(provider=user)
        return MatchRequest.objects.none()

    def create(self, request):
        """
        Robust match request creation with comprehensive error handling
        """
        # Prepare serializer with request context
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )

        try:
            # Validate serializer
            serializer.is_valid(raise_exception=True)

            # Create match request (seeker will be set automatically)
            match_request = serializer.save()

            # Return created match request
            return Response(
                self.get_serializer(match_request).data,
                status=status.HTTP_201_CREATED
            )

        except ValidationError as val_error:
            # Handle validation errors
            return Response({
                'errors': val_error.detail
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as unexpected_error:
            # Handle any unexpected errors
            return Response({
                'error': 'Unexpected error during match request creation',
                'details': str(unexpected_error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['POST'])
    def find_matches(self, request):
        """
        Find potential matches based on seeker preferences
        """
        seeker_preferences = request.data
        matching_services = MatchingService.find_matching_services(seeker_preferences)

        matches = []

        for service in matching_services:
            match_score = calculate_match_score(request.user, service.provider)
            matches.append({
                'service': ServiceSerializer(service).data,
                'match_score': match_score
            })

        return Response(matches)

    def partial_update(self, request, pk=None):
        """
        Handle PATCH requests to update match request status
        """
        try:
            # Retrieve the match request
            match_request = self.get_object()

            # Validate status is provided in request
            status_update = request.data.get('status')

            if not status_update:
                return Response({
                    'error': 'Status is required for update'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate status transition based on user type
            user = request.user

            if user.user_type == 'seeker':
                # Seekers cannot modify status
                raise PermissionDenied('Seekers cannot update match request status')

            elif user.user_type == 'provider':
                # Providers can only update status from 'pending'
                if match_request.status != 'pending':
                    return Response({
                        'error': 'Can only update status from pending state'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Allowed status transitions for providers
                allowed_statuses = ['accepted', 'rejected']

                if status_update not in allowed_statuses:
                    return Response({
                        'error': f'Invalid status. Allowed: {allowed_statuses}'
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Update the status
            match_request.status = status_update
            match_request.save()

            # Serialize and return updated match request
            serializer = self.get_serializer(match_request)
            return Response(serializer.data)

        except MatchRequest.DoesNotExist:
            return Response({
                'error': 'Match request not found'
            }, status=status.HTTP_404_NOT_FOUND)

        except PermissionDenied as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_403_FORBIDDEN)

        except Exception as unexpected_error:
            return Response({
                'error': 'Unexpected error during match request update',
                'details': str(unexpected_error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
