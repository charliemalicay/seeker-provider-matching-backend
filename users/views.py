# users/views.py
from rest_framework import viewsets, permissions, status
from django.contrib.auth import authenticate, login
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

import logging

from .models import User
from .serializers import UserSerializer

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Custom permission logic
        """
        if self.action in ['create', 'list']:
            # Allow unauthenticated user registration
            permission_classes = [permissions.AllowAny]
        else:
            # Require authentication for other actions
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """
        Custom registration endpoint
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'user_type': user.user_type
                },
                'message': 'User created successfully'
            }, status=status.HTTP_201_CREATED)

        except serializers.ValidationError as e:
            return Response({
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({'csrf_token': get_token(request)})

    def post(self, request):
        # Enhanced logging and debugging
        username = request.data.get('username')
        password = request.data.get('password')

        # Log incoming request details
        logger.info(f"Login attempt for username: {username}")

        # Comprehensive authentication debugging
        try:
            # Check if user exists
            User = get_user_model()
            try:
                user_exists = User.objects.filter(username=username).exists()
                logger.info(f"User exists: {user_exists}")
            except Exception as e:
                logger.error(f"Error checking user existence: {e}")
                return Response({
                    'detail': 'Database error',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Detailed authentication
            user = authenticate(username=username, password=password)

            if user is not None:
                # Check if user is active
                if user.is_active:
                    login(request, user)
                    logger.info(f"Successful login for user: {username}")
                    return Response({
                        'detail': 'Successfully logged in',
                        'user_id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'user_type': getattr(user, 'user_type', None)
                    }, status=status.HTTP_200_OK)
                else:
                    logger.warning(f"Inactive user login attempt: {username}")
                    return Response({
                        'detail': 'User account is not active'
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                # More detailed error logging
                logger.warning(f"Failed login attempt for username: {username}")

                # Check if username exists to provide more specific feedback
                try:
                    user_with_username = User.objects.filter(username=username).first()
                    if user_with_username:
                        return Response({
                            'detail': 'Invalid password',
                            'error_code': 'INVALID_PASSWORD'
                        }, status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        return Response({
                            'detail': 'User not found',
                            'error_code': 'USER_NOT_FOUND'
                        }, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    logger.error(f"Error during login verification: {e}")
                    return Response({
                        'detail': 'Authentication system error',
                        'error': str(e)
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"Unexpected error during login: {e}")
            return Response({
                'detail': 'Unexpected authentication error',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
