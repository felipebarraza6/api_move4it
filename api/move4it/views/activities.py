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
from api.move4it.models import ActivityCategory, Activity, RegisterActivity, FileRegisterActivity
from api.move4it.serializers import ActivityCategorySerializer, ActivitySerializer, RegisterActivitySerializer, FileRegisterActivitySerializer


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
                'is_global': ['exact'],
            }
    filterset_class = FilterActivity
    queryset = Activity.objects.all()
    lookup_field = 'id'


class RegisterActivityViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,):

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    serializer_class = RegisterActivitySerializer
    filter_backends = (filters.DjangoFilterBackend,)

    class FilterRegisterActivity (filters.FilterSet):
        class Meta:
            model = RegisterActivity
            fields = {
                "start_date_time": ['exact', 'gt', 'lt', 'gte', 'lte', "year", "month", "day", "week_day", "hour", "minute", "second", "date", "time", "isnull", "regex", "iregex"],
                "activity": ['exact'],
                "groups": ['exact'],
            }
    filterset_class = FilterRegisterActivity
    queryset = RegisterActivity.objects.all()
    lookup_field = 'id'

class FileRegisterActivityViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,):

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    serializer_class = FileRegisterActivitySerializer
    filter_backends = (filters.DjangoFilterBackend,)

    class FilterFileRegisterActivity (filters.FilterSet):
        class Meta:
            model = FileRegisterActivity
            fields = {
                'register_activity': ['exact'],
            }
    filterset_class = FilterFileRegisterActivity
    queryset = FileRegisterActivity.objects.all()
    lookup_field = 'id'
