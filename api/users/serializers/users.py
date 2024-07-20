# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Django
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator

# Models
from api.users.models import User, Profile, CorporalMeditions, SportActivity, PreviousIllnesse
from api.move4it.models import Enterprise, Group, ActivityCategory, TypeMedition, RegisterActivity, Competence, Enterprise, FileRegisterActivity
from api.move4it.serializers import EnterpriseSerializer, ActivitySerializer 
from .profiles import  SportActivityModelSerializer, PreviousIllnesseModelSerializer


class CorporalMeditionsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorporalMeditions
        fields = '__all__'

class RegisterActivitySerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()
    class Meta:
        model = RegisterActivity
        fields = '__all__'


class TypeMeditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeMedition
        fields = '__all__'


class ProfileModelSerializer(serializers.ModelSerializer):
    corporal_meditions = serializers.SerializerMethodField('get_corporal_meditions')
    groups = serializers.SerializerMethodField('get_groups')
    total_activities_group = serializers.SerializerMethodField('get_activities_group')
    total_activities_group_completed = serializers.SerializerMethodField('get_activities_group_completed')
    total_activities_user = serializers.SerializerMethodField('get_activities_user')
    type_meditions = serializers.SerializerMethodField('get_type_meditions')
    challengers_user = serializers.SerializerMethodField('get_challengers_user')

    def get_challengers_user(self, profile):
        groups = RegisterActivity.objects.filter(users=profile.user.id, activity__is_challenge=True)
        return RegisterActivitySerializer(groups, many=True).data


    def get_type_meditions(self, profile):
        groups = TypeMedition.objects.all()
        return TypeMeditionSerializer(groups, many=True).data

    def get_activities_user(self, profile):
        groups = RegisterActivity.objects.filter(users=profile.user.id, is_user=True)
        return RegisterActivitySerializer(groups, many=True).data

    def get_activities_group(self, profile):
        groups = RegisterActivity.objects.filter(groups=profile.user.group_participation.id, is_group=True)
        return RegisterActivitySerializer(groups, many=True).data

    def get_activities_group_completed(self, profile):
        groups = RegisterActivity.objects.filter(groups=profile.user.group_participation.id, is_group=True, is_completed=True)
        return RegisterActivitySerializer(groups, many=True).data

    def get_groups(self, profile):
        groups = Group.objects.filter(enterprise=profile.user.group_participation.enterprise.id)
        return GroupSerializer(groups, many=True).data

    def get_corporal_meditions(self, profile):
        groups = CorporalMeditions.objects.filter(profile=profile)
        return CorporalMeditionsModelSerializer(groups, many=True).data

    class Meta:
        model = Profile
        fields = '__all__'


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    enterprise = serializers.SerializerMethodField('get_enterprise')

    def get_enterprise(self, group):
        groups = Enterprise.objects.filter(group=group).first()
        return EnterpriseSerializer(groups, many=False).data

    class Meta:
        model = Group
        fields = '__all__'




class UserResponseSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField('get_team')
    profile = serializers.SerializerMethodField('get_profile')
    
    def get_profile(self, user):
        groups = Profile.objects.filter(user=user).first()
        return ProfileModelSerializer(groups, many=False).data
    
    def get_team(self, user):
        groups = Group.objects.filter(user=user).first()
        return GroupSerializer(groups, many=False).data



    class Meta:
        model = User
        fields = "__all__"

class ResetPasswordSerializer(serializers.Serializer):
    user = serializers.EmailField()
    new_password = serializers.CharField(min_length=6, max_length=64)

    def validate(self, data):
        user = data['user']
        try:
            get_user = User.objects.get(email=user)
            data_email = get_user.email
        except:
            raise serializers.ValidationError('El usuario no existe!')
        get_user.set_password(data['new_password'])
        get_user.save()

        return data


class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Credenciales Invalidas')
        if not user.is_verified:
            raise serializers.ValidationError(
                'Cuenta de usuario aun no verificada')
        self.context['user'] = user
        return data

    def create(self, data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class UserSignUpSerializer(serializers.Serializer):

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    first_name = serializers.CharField(max_length=500)

    last_name = serializers.CharField(max_length=500)

    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    identification_number = serializers.CharField(
        max_length=13,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    phone_number = serializers.CharField(
        max_length=13,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    type_user = serializers.CharField(max_length=3)

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Contraseñas no coinciden")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_active=True)
        Profile.objects.create(user=user)
        return data
