from rest_framework import mixins, viewsets

# Filters
from django_filters import rest_framework as filters

# Permissions
from rest_framework.permissions import IsAuthenticated

# Models
from api.move4ia.models import RegisterActivity, FileRegisterActivity
from api.move4ia.serializers import RegisterActivitySerializer, FileRegisterActivitySerializer


class RegisterActivityViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    """ViewSet for handling RegisterActivity operations."""

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = RegisterActivitySerializer
    lookup_field = 'id'

    queryset = RegisterActivity.objects.all()

    class FilterRegisterActivity(filters.FilterSet):
        """FilterSet for RegisterActivity."""
        class Meta:
            """Meta class for FilterRegisterActivity."""
            model = RegisterActivity
            fields = {
                'interval': ['exact'],
                'user': ['exact'],
            }

    filterset_class = FilterRegisterActivity


class FileRegisterActivityViewSet(mixins.CreateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.ListModelMixin,
                                  mixins.DestroyModelMixin,
                                  viewsets.GenericViewSet):
    """ViewSet for handling FileRegisterActivity operations."""

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    serializer_class = FileRegisterActivitySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = FileRegisterActivity.objects.all()
    lookup_field = 'id'

    class FilterFileRegisterActivity (filters.FilterSet):
        class Meta:
            model = FileRegisterActivity
            fields = {
                'register_activity': ['exact'],
            }
    filterset_class = FilterFileRegisterActivity
