from rest_framework import mixins, viewsets, status

# Filters
from django_filters import rest_framework as filters

# Permissions
from rest_framework.permissions import (
    IsAuthenticated
)


# Models
from api.move4ia.models import ActivityCategory, Activity
from api.move4ia.serializers import ActivityCategorySerializer, ActivitySerializer


class CategoryActivityViewSet(mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet,):

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    serializer_class = ActivityCategorySerializer
    filter_backends = (filters.DjangoFilterBackend,)

    class FilterCategoryActivity (filters.FilterSet):
        class Meta:
            model = ActivityCategory
            fields = {
                'name': ['exact'],
            }
    filterset_class = FilterCategoryActivity
    queryset = ActivityCategory.objects.all()
    lookup_field = 'id'


class ActivityViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet,):

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    serializer_class = ActivitySerializer
    filter_backends = (filters.DjangoFilterBackend,)

    class FilterActivity (filters.FilterSet):
        class Meta:
            model = Activity
            fields = {
                'name': ['exact'],
                'category': ['exact'],
                'type_medition': ['exact'],
            }
    filterset_class = FilterActivity
    queryset = Activity.objects.all()
    lookup_field = 'id'
