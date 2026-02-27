from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.db.models import Q
from freelance_arena.utils import success_response
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    AdminUserSerializer,
    FreelancerSearchSerializer,
)
from .permissions import IsAdminRole


class RegisterView(APIView):
    '''POST - Register a new user (CLIENT or FREELANCER).'''
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return success_response(
            data={
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
            },
            message='Registration successful.',
            status_code=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    '''POST - Login with email and password, returns JWT tokens.'''
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return success_response(
            data={
                'user_id': str(user.id),
                'role': user.role,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
            },
            message='Login successful.',
        )


class LogoutView(APIView):
    '''POST - Logout by blacklisting the refresh token.'''
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return success_response(
                    data=None,
                    message='Refresh token is required.',
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return success_response(message='Logout successful.')
        except TokenError:
            return success_response(
                data=None,
                message='Token is invalid or already blacklisted.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class ProfileView(APIView):
    '''GET/PUT/PATCH/DELETE own profile.'''
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return success_response(data=serializer.data, message='Profile retrieved.')

    def put(self, request):
        serializer = UserProfileSerializer(
            request.user, data=request.data, partial=False
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(data=serializer.data, message='Profile updated.')

    def patch(self, request):
        serializer = UserProfileSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(data=serializer.data, message='Profile updated.')

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save(update_fields=['is_active'])
        return success_response(message='Account deactivated successfully.')


class ChangePasswordView(APIView):
    '''POST - Change password for authenticated user.'''
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save(update_fields=['password'])
        return success_response(message='Password changed successfully.')


class UserListView(generics.ListAPIView):
    '''GET - Admin only. List all users with filters.'''
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'username', 'email']
    ordering = ['-date_joined']

    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.query_params.get('role')
        is_active = self.request.query_params.get('is_active')

        if role:
            queryset = queryset.filter(role=role)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(data=response.data, message='Users retrieved.')


class UserDetailAdminView(APIView):
    '''GET/PUT/DELETE - Admin only. Manage any user account.'''
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def get(self, request, user_id):
        user = self.get_user(user_id)
        if not user:
            return success_response(
                data=None,
                message='User not found.',
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = AdminUserSerializer(user)
        return success_response(data=serializer.data, message='User retrieved.')

    def put(self, request, user_id):
        user = self.get_user(user_id)
        if not user:
            return success_response(
                data=None,
                message='User not found.',
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = AdminUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(data=serializer.data, message='User updated.')

    def delete(self, request, user_id):
        user = self.get_user(user_id)
        if not user:
            return success_response(
                data=None,
                message='User not found.',
                status_code=status.HTTP_404_NOT_FOUND,
            )
        user.is_active = False
        user.save(update_fields=['is_active'])
        return success_response(message='User deactivated.')


class FreelancerSearchView(generics.ListAPIView):
    '''GET - Public. Search freelancers by skills and username.'''
    serializer_class = FreelancerSearchSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'skills', 'first_name', 'last_name']
    ordering_fields = ['hourly_rate', 'username']

    def get_queryset(self):
        queryset = User.objects.filter(role='FREELANCER', is_active=True)
        skills = self.request.query_params.get('skills')
        if skills:
            skill_list = [s.strip() for s in skills.split(',')]
            q = Q()
            for skill in skill_list:
                q |= Q(skills__icontains=skill)
            queryset = queryset.filter(q)
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(data=response.data, message='Freelancers retrieved.')
