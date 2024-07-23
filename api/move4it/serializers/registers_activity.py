"""Serializers Registers Activity."""

from rest_framework import serializers
from api.move4it.models import RegisterActivity, FileRegisterActivity


class RegisterActivitySerializer(serializers.ModelSerializer):
    """Register activity serializer."""
    class Meta:
        """Meta class."""
        model = RegisterActivity
        fields = '__all__'


class FileRegisterActivitySerializer(serializers.ModelSerializer):
    """File register activity serializer."""
    class Meta:
        """Meta class."""
        model = FileRegisterActivity
        fields = '__all__'
