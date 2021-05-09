"""Users views."""

# Django REST Framework
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from cassie.users.permissions import IsAccoutOwner, IsAdminOrAccountOwner

# Serializers
from cassie.users.serializers import (
  UserLoginSerializer,
  UserModelSerializer,
  UserSignUpSerializer,
  AccountVerificationSerializer,
  UserTokenRefreshSerializer
)

# Models
from cassie.users.models import User
from cassie.licenses.models import License

class UserLoginView(TokenObtainPairView):
  """User login view."""
  serializer_class = UserLoginSerializer

class UserTokenRefreshView(TokenRefreshView):
  """Custom user token refresh view."""
  serializer_class = UserTokenRefreshSerializer

class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
  """User view set.
    Handle sign up and account verification.
  """

  queryset = User.objects.filter(is_active=True)
  serializer_class = UserModelSerializer
  lookup_field = 'username'

  def get_permissions(self):
    """Assing permissions based on action."""
    if self.action in ['signup', 'login', 'verify']:
      permissions = [AllowAny]
    elif self.action in ['update', 'partial_update']:
      permissions = [IsAuthenticated, IsAccoutOwner]
    elif self.action == 'retrieve':
      permissions = [IsAuthenticated, IsAdminOrAccountOwner]
    else:
      permissions = [IsAuthenticated]
    return [permission() for permission in permissions]

  @action(detail=False, methods=['POST'])
  def signup(self, request):
    """User sign up."""
    serializer = UserSignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    data = UserModelSerializer(user).data
    return Response(data, status=status.HTTP_201_CREATED)

  @action(detail=False, methods=['POST'])
  def verify(self, request):
    """User account verification."""
    serializer = AccountVerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    data = { 'message': 'Congratulation, your account is active now.' }
    return Response(data, status=status.HTTP_200_OK)
