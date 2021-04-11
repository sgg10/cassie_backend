"""Users Serializers."""
# Django
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from django.conf import settings

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.state import token_backend

# Model
from cassie.users.models import User

# Task
from cassie.taskapp.tasks import send_cofirmation_email

# Utilities
import jwt
from datetime import timedelta

# Serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

class UserModelSerializer(serializers.ModelSerializer):
  """User model serializer."""

  class Meta:
    """Meta class."""
    model = User
    fields = (
      'username',
      'first_name',
      'last_name',
      'email',
      'phone_number'
    )

class UserLoginSerializer(TokenObtainPairSerializer):
  """User login serializer.
    Handle the login request data.
  """

  def validate(self, attrs):
    """Check credentials and get token."""
    user = authenticate(username=attrs['email'], password=attrs['password'])
    if not user:
      raise serializers.ValidationError('Invalid credentials.')
    if not user.is_verified:
      raise serializers.ValidationError('Account is not active yet.')

    refresh = self.get_token(user)
    data = {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserModelSerializer(user).data
    }
    return data

class UserSignUpSerializer(serializers.Serializer):
  """User sign up serializer.
    Handle sign up data validation and user/profile creation.
  """

  email = serializers.EmailField(
    validators=[UniqueValidator(queryset=User.objects.all())]
  )

  username = serializers.CharField(
    min_length=4,
    max_length=20,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )

  # Phone number
  phone_regex = RegexValidator(
    regex=r'\+?1?\d{9,15}$',
    message='Phone number must be entered in the format: +9 99999999. Up to 15 digits allowed.'
  )
  phone_number = serializers.CharField(validators=[phone_regex])

  # Password
  password = serializers.CharField(min_length=8)
  password_confirmation = serializers.CharField(min_length=8)

  # Name
  first_name = serializers.CharField(min_length=2, max_length=30)
  last_name = serializers.CharField(min_length=2, max_length=30)

  def validate(self, data):
    """Verify passwords match."""
    passwd = data['password']
    passwd_conf = data['password_confirmation']
    if passwd != passwd_conf:
      raise serializers.ValidationError("Passwords don't match.")
    password_validation.validate_password(passwd)
    return data

  def create(self, data):
    """Handle user creation."""
    data.pop('password_confirmation')
    user = User.objects.create_user(**data, is_verified=False, is_admin=False)
    send_cofirmation_email.delay(user_pk=user.pk)
    return user

class AccountVerificationSerializer(serializers.Serializer):
  """Acount verification serializer."""

  token = serializers.CharField()

  def validate_token(self, data):
    """Verify token is valid."""
    try:
      payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise serializers.ValidationError('Verification link has expired')
    except jwt.PyJWTError:
      raise serializers.ValidationError('Invalid token.')

    if payload['type'] != 'email_confirmation':
      raise serializers.ValidationError('Invalid token.')

    self.context['payload'] = payload
    return data

  def save(self):
    """Update user's varified status."""
    payload = self.context['payload']
    user = User.objects.get(username=payload['user'])
    user.is_verified = True
    user.save()

class UserTokenRefreshSerializer(TokenRefreshSerializer):
  """User token refresh serializer."""

  def validate(self, attrs):
    data = super(UserTokenRefreshSerializer, self).validate(attrs)
    decoded_payload = token_backend.decode(data['access'], verify=True)
    user_id = decoded_payload['user_id']
    data['user'] = UserModelSerializer(User.objects.get(id=user_id)).data
    return data