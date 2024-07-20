# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Django
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator

# Models
from api.move4it.models import Blog


class BlogModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields = ['id', 'created', 'modified']
