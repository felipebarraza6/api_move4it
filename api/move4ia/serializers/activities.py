"""Activities Serialiserz."""
from rest_framework import serializers
from api.move4ia.models import Activity, ActivityCategory


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class ActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = '__all__'


class ActivitySerializerForm(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
