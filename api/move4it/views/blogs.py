from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import action

from rest_framework import status
from rest_framework import mixins, viewsets, status


from rest_framework import generics

# Filters
from django_filters import rest_framework as filters

# Permissions
from rest_framework.permissions import (
    IsAuthenticated
)


# Models
from api.move4it.models import Blog
from api.move4it.serializers import BlogModelSerializer


class BlogViewSet(mixins.RetrieveModelMixin,
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
            return BlogModelSerializer
        else:
            return BlogModelSerializer

    filter_backends = (filters.DjangoFilterBackend,)

    class FilterBlog (filters.FilterSet):
        class Meta:
            model = Blog
            fields = {
                'type': ['exact'],
            }
    filterset_class = FilterBlog
    queryset = Blog.objects.all()
    lookup_field = 'id'
