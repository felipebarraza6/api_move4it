"""User serializers."""
# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Django
from django.contrib.auth import password_validation, authenticate

# Models
from api.users.models import User, Profile, CorporalMeditions
from api.move4it.models import Enterprise, Group, TypeMedition, RegisterActivity, Competence
from api.move4it.serializers import EnterpriseSerializer


class CorporalMeditionsModelSerializer(serializers.ModelSerializer):
    """Corporal meditions."""
    class Meta:
        """Meta class."""
        model = CorporalMeditions
        fields = '__all__'


class RegisterActivitySerializer(serializers.ModelSerializer):
    """Register Activity."""

    class Meta:
        """Meta class."""
        model = RegisterActivity
        fields = '__all__'
        depth = 2


class TypeMeditionSerializer(serializers.ModelSerializer):
    """Type Medition."""
    class Meta:
        """Meta class."""
        model = TypeMedition
        fields = '__all__'


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""
    corporal_meditions = serializers.SerializerMethodField(
        'get_corporal_meditions')

    def get_corporal_meditions(self, profile):
        """get corporal meditions."""
        groups = CorporalMeditions.objects.filter(
            profile=profile.id).order_by('-created').all()
        return CorporalMeditionsModelSerializer(groups, many=True).data

    class Meta:
        """Meta class."""
        model = Profile
        fields = '__all__'


class UserModelSerializer(serializers.ModelSerializer):
    """Base Inline User Model Serializer."""
    class Meta:
        """Meta class."""
        model = User
        fields = '__all__'


class UserShortModelSerializer(serializers.ModelSerializer):
    """User Short Model Serializer."""
    class Meta:
        """Meta class."""
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email',
                  'phone_number', 'identification_number', 'type_user')


class CompetenceModelSerializer(serializers.ModelSerializer):
    """Competence model serializer."""
    class Meta:
        """Meta class."""
        model = Competence
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    """Group model serializer."""
    competition = serializers.SerializerMethodField('get_enterprise')

    def get_enterprise(self, group):
        """get enterprise."""
        request = self.context['request']
        groups = Enterprise.objects.filter(group=group).first()
        return EnterpriseSerializer(groups, many=False, context={'request': request}).data

    class Meta:
        """Meta class."""
        model = Group
        fields = ('id', 'name', 'competition')


class UserResponseSerializer(serializers.ModelSerializer):
    """User model serializer."""
    enterprise_competition_overflow = serializers.SerializerMethodField(
        'get_enterprise')
    profile = serializers.SerializerMethodField('get_profile')

    def get_enterprise(self, group):
        """get enterprise."""
        request = self.context['request']
        groups = Enterprise.objects.filter(
            group=group.group_participation).first()
        return EnterpriseSerializer(groups, many=False, context={'request': request}).data

    def get_profile(self, user):
        """get profile."""
        groups = Profile.objects.filter(user=user).first()
        return ProfileModelSerializer(groups, many=False).data

    def get_team(self, user):
        """get team."""
        request = self.context['request']
        groups = Group.objects.filter(user=user).first()
        return GroupSerializer(groups, many=False, context={'request': request}).data

    class Meta:
        """Meta class."""
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'phone_number',
                  'identification_number', 'type_user', 'enterprise_competition_overflow', 'profile')


class ResetPasswordSerializer(serializers.Serializer):
    """Reset password serializer."""

    user = serializers.EmailField()
    new_password = serializers.CharField(min_length=6, max_length=64)

    def validate(self, attrs):
        user = attrs['user']
        try:
            get_user = User.objects.get(email=user)
        except Exception as exc:
            raise serializers.ValidationError('El usuario no existe!') from exc
        get_user.set_password(attrs['new_password'])
        get_user.save()

        return attrs


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
