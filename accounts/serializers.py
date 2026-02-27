from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'role', 'password', 'confirm_password',
        ]
        read_only_fields = ['id']

    def validate_role(self, value):
        if value not in ('CLIENT', 'FREELANCER'):
            raise serializers.ValidationError(
                'Role must be either CLIENT or FREELANCER.'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'A user with this email already exists.'
            )
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {'confirm_password': 'Passwords do not match.'}
            )
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid credentials.')

        if not user.is_active:
            raise serializers.ValidationError('Account is deactivated.')

        data['user'] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile view and update."""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'role', 'bio', 'profile_picture', 'skills', 'hourly_rate',
            'is_active', 'date_joined', 'last_seen', 'email_verified',
            'full_name',
        ]
        read_only_fields = ['id', 'email', 'date_joined', 'role', 'is_active']

    def validate_profile_picture(self, value):
        if value and value.size > 2 * 1024 * 1024:  # 2MB
            raise serializers.ValidationError(
                'Profile picture must be less than 2MB.'
            )
        return value

    def validate_skills(self, value):
        if value:
            # Validate comma-separated format
            skills = [s.strip() for s in value.split(',')]
            if any(len(s) == 0 for s in skills):
                raise serializers.ValidationError(
                    'Skills must be a comma-separated list with no empty entries.'
                )
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password."""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {'confirm_password': 'New passwords do not match.'}
            )
        return data


class AdminUserSerializer(serializers.ModelSerializer):
    """Full user serializer for admin use."""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'role', 'bio', 'profile_picture', 'skills', 'hourly_rate',
            'is_active', 'is_staff', 'date_joined', 'last_seen',
            'email_verified', 'full_name',
        ]
        read_only_fields = ['id', 'date_joined']


class FreelancerSearchSerializer(serializers.ModelSerializer):
    """Lightweight serializer for freelancer search results."""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'full_name',
            'bio', 'profile_picture', 'skills', 'hourly_rate',
        ]
