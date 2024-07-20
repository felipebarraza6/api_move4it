from rest_framework import mixins, viewsets, status, generics
# Filters
from django_filters import rest_framework as filters

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)


# Models
from api.users.models import Profile, SportActivity, PreviousIllnesse# Serializers
from api.users.serializers import ProfileModelSerializer, SportActivityModelSerializer, PreviousIllnesseModelSerializer 


class ProfileViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,):

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return ProfileModelSerializer
        else:
            return ProfileModelSerializer

    filter_backends = (filters.DjangoFilterBackend,)

    class FilterProfile (filters.FilterSet):
        class Meta:
            model = Profile
            fields = {
                'user': ['exact'],
                "date_of_birth": ['exact'],
                "target_weight": ['exact'],
                "target_fat": ['exact'],
                "sports_activities": ['exact'],
                "previous_illnesses": ['exact'],
            }

    filterset_class = FilterProfile
    queryset = Profile.objects.all()
    lookup_field = 'id'

class SportActivityViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,):

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    serializer_class = SportActivityModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    class FilterSportActivity (filters.FilterSet):
        class Meta:
            model = SportActivity
            fields = {
                'name': ['exact'],
            }
    filterset_class = FilterSportActivity
    queryset = SportActivity.objects.all()
    lookup_field = 'id'

class PreviousIllnesseViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,):

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    serializer_class = PreviousIllnesseModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    class FilterPreviousIllnesse (filters.FilterSet):
        class Meta:
            model = PreviousIllnesse
            fields = {
                'name': ['exact'],
            }
    filterset_class = FilterPreviousIllnesse
    queryset = PreviousIllnesse.objects.all()
    lookup_field = 'id'


