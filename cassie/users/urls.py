"""Users URLs."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# DRF Simple JWT
from rest_framework_simplejwt.views import TokenRefreshView

# Views
from .views import users as user_views

router = DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')

urlpatterns = [
  path('users/login/', user_views.UserLoginView.as_view(), name='login'),
  path('users/refresh/', user_views.UserTokenRefreshView.as_view(), name='token_refresh'),
  path('', include(router.urls))
]
