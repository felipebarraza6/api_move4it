from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Django
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator

# Models
from api.users.models import Profile, CorporalMeditions, SportActivity, PreviousIllnesse


class ProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class CorporalMeditionsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorporalMeditions
        fields = '__all__'

class SportActivityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportActivity
        fields = '__all__'

class PreviousIllnesseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviousIllnesse
        fields = '__all__'


