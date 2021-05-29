"""Users URLs."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# DRF Simple JWT
from rest_framework_simplejwt.views import TokenRefreshView

# Views
from .views import users as user_views
from .views import licenses as user_licenses_views
from .views import accounts as user_accounts_views

router = DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')
router.register(
  r'users/(?P<username>[-a-zA-Z0-9_-]+)/licenses',
  user_licenses_views.UserLicensesViewSet,
  basename='users_licenses'
)
router.register(
  r'users/(?P<username>[-a-zA-Z0-9_-]+)/accounts',
  user_accounts_views.UserAccountViewSet,
  basename='users_accounts'
)

urlpatterns = [
  path('users/login/', user_views.UserLoginView.as_view(), name='login'),
  path('users/refresh/', user_views.UserTokenRefreshView.as_view(), name='token_refresh'),
  path('', include(router.urls))
]
