"""License URLs."""

# Django
from django.urls import path, include

# Django REST Framwork
from rest_framework.routers import DefaultRouter

# Views
from .views import licenses as licenses_views

router = DefaultRouter()
router.register(r'licenses', licenses_views.LicenseViewSet, basename='licenses')

urlpatterns = [
  path('', include(router.urls))
]