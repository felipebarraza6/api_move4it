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
    AllowAny,
    IsAuthenticated
)


# Models
from api.users.models import User, CorporalMeditions
# Serializers
from api.users.serializers import CorporalMeditionsModelSerializer, ResetPasswordSerializer, UserResponseSerializer, UserLoginSerializer, UserModelSerializer, UserSignUpSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,):

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['login', 'signup']:
            permissions = [AllowAny]
        elif self.action in ['retrieve']:
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return UserResponseSerializer
        else:
            return UserModelSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    queryset = User.objects.filter(is_verified=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    class FilterUser(filters.FilterSet):
        class Meta:
            model = User
            fields = {
                'username': ['exact'],
                'email': ['exact'],
                "first_name": ['exact'],
                "last_name": ['exact'],
                "is_leader": ['exact'],
            }

    filterset_class = FilterUser

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'message': 'ACTUALIZADO'
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()

        data = {
            'user': UserResponseSerializer(user).data,
            'access_token': token,

        }

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserResponseSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """Add extra data to the response."""
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)

        data = {
            'user': response.data,
        }

        response.data = data
        return response


class CorporalMeditionsViewSet(mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet,):

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return CorporalMeditionsModelSerializer
        else:
            return CorporalMeditionsModelSerializer

    filter_backends = (filters.DjangoFilterBackend,)

    class FilterCorporalMedition(filters.FilterSet):
        class Meta:
            model = CorporalMeditions
            fields = {
                'profile': ['exact'],
                'weight': ['exact'],
                "fat": ['exact'],
                "created": ['exact', 'gte', 'lte', 'lt', 'gt', 'year', 'month', 'day', 'week_day', 'hour', 'minute', 'second', 'isnull', 'regex', 'iregex'],
            }

    filterset_class = FilterCorporalMedition

    queryset = CorporalMeditions.objects.all()
    serializer_class = CorporalMeditionsModelSerializer
    lookup_field = 'id'
