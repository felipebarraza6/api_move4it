from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import mixins, viewsets

# Filters
from django_filters import rest_framework as filters

# Permissions
from rest_framework.permissions import IsAuthenticated

# Models
from api.move4it.models import RegisterActivity
from api.move4it.serializers import RegisterActivitySerializer


class RegisterActivityViewSet(mixins.RetrieveModelMixin,
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
