from rest_framework import serializers
from api.move4it.models import Activity, ActivityCategory, RegisterActivity, FileRegisterActivity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class ActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = '__all__'


class RegisterActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterActivity
        fields = '__all__'

class FileRegisterActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FileRegisterActivity
        fields = '__all__'

