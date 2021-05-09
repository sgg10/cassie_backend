"""Accounts URLs."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import accounts as accounts_views

router = DefaultRouter()
router.register(r'accounts', accounts_views.AccountViewSet, basename='accounts')
router.register(r'accounts/bot', accounts_views.AccountAuthorizationViewset, basename='accountsAuth')

urlpatterns = [
  path('', include(router.urls))
]