"""Urls Customers."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from api.users.views import users as views_users, profiles as views_profile 

router = DefaultRouter()

# Actions
router.register(r'users', views_users.UserViewSet, basename='users')
router.register(
    r'meditions', views_users.CorporalMeditionsViewSet, basename='meditions')
router.register(r'profiles', views_profile.ProfileViewSet, basename='profiles')
router.register(
    r'sports-activities', views_profile.SportActivityViewSet, basename='sports-activities')
router.register(r'previous-illnesses', views_profile.PreviousIllnesseViewSet,
                basename='previous-illnesses')

urlpatterns = [
    path('', include(router.urls))
]
