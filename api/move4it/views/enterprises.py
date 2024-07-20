from rest_framework import status
from rest_framework import mixins, viewsets, status


from rest_framework import generics

# Filters
from django_filters import rest_framework as filters

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)


# Models
from api.move4it.models import Competence, Enterprise, Group 
from api.move4it.serializers import CompetenceSerializer, EnterpriseSerializer, GroupSerializerList, GroupSerializer


class CompetenceViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,):

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = CompetenceSerializer

    class FilterCompetence (filters.FilterSet):
        class Meta:
            model = Competence
            fields = {
                'name': ['icontains'],
            }
    filterset_class = FilterCompetence
    queryset = Competence.objects.all()
    lookup_field = 'id'


class EnterpriseViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,):

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = EnterpriseSerializer

    class FilterEnterprise(filters.FilterSet):
        class Meta:
            model = Enterprise
            fields = {
                'name': ['icontains'],
            }
    filterset_class = FilterEnterprise
    queryset = Enterprise.objects.all()
    lookup_field = 'id'


class GroupViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,):

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    filter_backends = (filters.DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action in ['list']:
            return GroupSerializerList
        else:
            return GroupSerializer

    class FilterGroup (filters.FilterSet):
        class Meta:
            model = Group
            fields = {
                'name': ['icontains'],
            }
    filterset_class = FilterGroup
    queryset = Group.objects.all()
    lookup_field = 'id'


