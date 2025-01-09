from django.db.models.base import Model
from rest_framework import serializers
from api.move4it.models import Enterprise, Group, Competence, Interval, RegisterActivity, FileRegisterActivity
from api.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'group_participation')
        depth = 2
        
class FileRegisterActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FileRegisterActivity
        fields = '__all__'

class RegisterActivitySerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField('get_files')
    users = UserSerializer(many=True)
    
    def get_files(self, register_activity):
        files = FileRegisterActivity.objects.filter(register_activity=register_activity).all()
        serialized_files = FileRegisterActivitySerializer(files, many=True).data
        return serialized_files
    class Meta:
        model = RegisterActivity
        fields = ('id', 'start_date_time', 'finish_date_time', 'activity','location', 'value', 'is_active','is_load','is_completed', 'observation', 'location', 'files','users')
        depth = 3

class IntervalSerializer(serializers.ModelSerializer):
    assignations = serializers.SerializerMethodField('get_activities')
    assignations_team = serializers.SerializerMethodField('get_activities_team')
    
    def get_activities_team(self, interval):
        group_participation = self.context.get('request').user.group_participation
        activities = RegisterActivity.objects.filter(interval=interval, is_active=True, users__group_participation=group_participation).all()
        serialized_activities = RegisterActivitySerializer(activities, many=True).data
        
        def get_total_points_completed(interval):
            activities = RegisterActivity.objects.filter(interval=interval, is_active=True, is_completed=True, users__group_participation=group_participation.id).all()
            total_points = 0
            divide = 1
            for activity in activities:
                total_points += activity.activity.points
            
            if len(activities) > 1:
                divide = len(activities)
                
            return int(total_points / divide)
    
        def get_total_points(interval):
            activities = RegisterActivity.objects.filter(interval=interval, is_active=True, users__group_participation=group_participation).all()
            total_points = 0
            divide = 1
            for activity in activities:
                total_points += activity.activity.points
            if len(activities) > 1:
                divide = len(activities)
            
            return int(total_points / divide)
        
        def get_quantity_participants(interval):
            activities = RegisterActivity.objects.filter(interval=interval, is_active=True, users__group_participation=group_participation).all()
            quantity_participants = 0
            for activity in activities:
                quantity_participants += len(activity.users.all())
            return quantity_participants
    

        data_team = {
            'total_points': get_total_points(interval),
            'total_points_completed': get_total_points_completed(interval),
            'quantity_participants': get_quantity_participants(interval),
            'assignations': serialized_activities
        }
        return data_team

    def get_activities(self, interval):
        activities = RegisterActivity.objects.filter(interval=interval).all()
        serialized_activities = RegisterActivitySerializer(activities, many=True).data

        def get_total_points_completed(interval):
            activities = RegisterActivity.objects.filter(interval=interval, is_active=True, is_completed=True).all()
            total_points = 0
            divide = 1
            for activity in activities:
                total_points += activity.activity.points
            
            if len(activities) > 1:
                divide = len(activities)
                
            return int(total_points / divide)
    
        def get_total_points(interval):
            activities = RegisterActivity.objects.filter(interval=interval, is_active=True).all()
            total_points = 0
            divide = 1
            for activity in activities:
                total_points += activity.activity.points
            if len(activities) > 1:
                divide = len(activities)
            
            return int(total_points / divide)
        
        def get_quantity_participants(interval):
            activities = RegisterActivity.objects.filter(interval=interval, is_active=True).all()
            quantity_participants = 0
            for activity in activities:
                quantity_participants += len(activity.users.all())
            return quantity_participants
        
        data = {
            'total_points': get_total_points(interval),
            'total_points_completed': get_total_points_completed(interval),
            'quantity_participants': get_quantity_participants(interval),
            'assignations': serialized_activities
        }
        
        return data 

    
    
    
    class Meta:
        model = Interval
        fields = ('start_date', 'end_date', "assignations_team",'assignations', )
        depth = 3

class CompetenceSerializer(serializers.ModelSerializer):

    intervals = serializers.SerializerMethodField('get_intervals')

    def get_intervals(self, competence):
        request = self.context['request']
        intervals = Interval.objects.filter(competence=competence).all()
        serialized_intervals = IntervalSerializer(intervals, many=True, context={'request': request}).data
        return serialized_intervals


    class Meta:
        model = Competence
        fields = '__all__'
        depth = 2


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
