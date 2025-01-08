from django.db.models.base import Model
from rest_framework import serializers
from api.move4it.models import Enterprise, Group, Competence, Interval, RegisterActivity

class RegisterActivitySerializer(serializers.Serializer):
    class Meta:
        model = RegisterActivity
        fields =('__all__')

class IntervalSerializer(serializers.ModelSerializer):
    activities = serializers.SerializerMethodField('get_activities')
    
    def get_activities(self, interval):
        activity = RegisterActivity.objects.filter(interval=interval.id).all()
        serialized_activities = RegisterActivitySerializer(activity, many=True).data
        return serialized_activities

    class Meta:
        model = Interval
        fields = ('start_date', 'end_date', 'activities')

class CompetenceSerializer(serializers.ModelSerializer):

    intervals = serializers.SerializerMethodField('get_intervals')

    def get_intervals(self, competence):
        intervals = Interval.objects.filter(competence=competence).all()
        serialized_intervals = IntervalSerializer(intervals, many=True).data
        return serialized_intervals


    class Meta:
        model = Competence
        fields = '__all__'


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = '__all__'


class GroupSerializerList(serializers.ModelSerializer):
    enterprise = serializers.SerializerMethodField('get_enterprise')

    def get_enterprise(self, group):
        enterprises = Enterprise.objects.filter(id=group.enterprise.id).first()
        return EnterpriseSerializer(enterprises, many=False).data

    class Meta:
        model = Group
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
