"""Enterprise Serializer."""
from datetime import date
from rest_framework import serializers
from api.move4it.models import (Enterprise, Group, Competence,
                                Interval, RegisterActivity, FileRegisterActivity)
from api.users.models import CorporalMeditions
from api.users.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'is_active', 'group_participation')
        depth = 2


class FileRegisterActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FileRegisterActivity
        fields = '__all__'


class RegisterActivitySerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField('get_files')
    user = UserSerializer(many=False)

    def get_files(self, register_activity):
        files = FileRegisterActivity.objects.filter(
            register_activity=register_activity).all()
        serialized_files = FileRegisterActivitySerializer(
            files, many=True).data
        return serialized_files

    class Meta:
        model = RegisterActivity
        fields = ('id',  'activity', 'location', 'value', 'interval',
                  'is_active', 'is_load', 'is_completed', 'observation', 'location', 'files', 'user')
        depth = 3


class IntervalSerializer(serializers.ModelSerializer):
    assignations = serializers.SerializerMethodField('get_activities')
    assignations_team = serializers.SerializerMethodField(
        'get_activities_team')
    status = serializers.SerializerMethodField('set_status')

    def set_status(self, obj):
        """set status"""
        today = date.today()
        if obj.end_date < today:
            return "Finalizado"
        elif obj.start_date <= today and obj.end_date >= today:
            return "Activo"

    def get_activities_team(self, interval):
        group_participation = self.context.get(
            'request').user.group_participation
        activities = RegisterActivity.objects.filter(
            interval=interval, is_active=True, user__group_participation=group_participation).all()
        serialized_activities = RegisterActivitySerializer(
            activities, many=True).data

        def get_total_points_completed(interval):
            activities = RegisterActivity.objects.filter(
                interval=interval, is_active=True, is_completed=True, user__group_participation=group_participation.id).all()
            total_points = 0
            divide = 1
            for activity in activities:
                total_points += activity.activity.points

            if len(activities) > 1:
                divide = len(activities)

            return int(total_points / divide)

        def get_total_points(interval):
            activities = RegisterActivity.objects.filter(
                interval=interval, is_active=True, user__group_participation=group_participation).all()
            total_points = 0
            divide = 1
            for activity in activities:
                total_points += activity.activity.points
            if len(activities) > 1:
                divide = len(activities)

            return activities.count()

        def get_quantity_participants(interval):
            activities = RegisterActivity.objects.filter(
                interval=interval, is_active=True, user__group_participation=group_participation).all()
            quantity_participants = 0

            user_ids = set()
            for activity in activities:
                user_ids.add(activity.user.id)
            quantity_participants = len(user_ids)

            return quantity_participants

        data_team = {
            'count': get_total_points(interval),
            'total_points_completed': get_total_points_completed(interval),
            'quantity_participants': get_quantity_participants(interval),
            'assignations': serialized_activities
        }
        return data_team

    def get_activities(self, interval):
        activities = RegisterActivity.objects.filter(interval=interval).all()
        serialized_activities = RegisterActivitySerializer(
            activities, many=True).data

        def get_quantity_participants(interval):
            activities = RegisterActivity.objects.filter(
                interval=interval, is_active=True).all()
            quantity_participants = 0

            user_ids = set()
            for activity in activities:
                user_ids.add(activity.user.id)
            quantity_participants = len(user_ids)

            return quantity_participants

        def get_total_points_completed(interval):
            activities_complete = RegisterActivity.objects.filter(
                interval=interval, is_active=True, is_completed=True)

            activities = RegisterActivity.objects.filter(
                interval=interval, is_active=True).all()

            total_points = 0
            divide = 1

            for activity in activities_complete:
                total_points += activity.activity.points

            if len(activities) > 1:
                divide = len(activities)

            return int(total_points)

        def get_total_points(interval):
            activities_complete = RegisterActivity.objects.filter(
                interval=interval, is_active=True).all()
            activities = RegisterActivity.objects.filter(
                interval=interval, is_active=True).all()
            total_points = 0
            divide = 1
            for activity in activities_complete:
                total_points += activity.activity.points

            if len(activities) > 1:
                divide = len(activities)

            return activities.count()

        data = {
            'count': get_total_points(interval),
            'total_points_completed': get_total_points_completed(interval),
            'quantity_participants': get_quantity_participants(interval),
            'assignations': serialized_activities
        }

        return data

    class Meta:
        model = Interval
        fields = ('start_date', 'end_date',
                  'assignations_team', 'assignations', 'status')
        depth = 3


class CompetenceSerializer(serializers.ModelSerializer):

    intervals = serializers.SerializerMethodField('get_intervals')

    def get_intervals(self, competence):
        group_participation = self.context.get(
            'request').user.group_participation
        intervals = Interval.objects.filter(competence=competence).all()
        serialized_intervals = IntervalSerializer(
            intervals, many=True).data
        return serialized_intervals

    class Meta:
        model = Competence
        fields = '__all__'
        depth = 2


class CompetenceSelectSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField('get_stats')
    days_remaining_competence = serializers.SerializerMethodField(
        'get_days_remaining_competence')
    days_remaining_interval = serializers.SerializerMethodField(
        'get_days_remaining_interval')
    avg_corporal_meditions = serializers.SerializerMethodField(
        'get_avg_corporal_meditions')
    intervals_to_back = serializers.SerializerMethodField(
        'get_intervals_to_back')

    def get_intervals_to_back(self, competence):
        intervals = Interval.objects.filter(
            competence=competence).order_by('-end_date').all()
        serialized_intervals = []
        today = date.today()
        for interval in intervals:
            if interval.start_date <= today <= interval.end_date:
                current_interval = interval
                break
        else:
            current_interval = None

        if current_interval:
            intervals = [current_interval] + \
                [interval for interval in intervals if interval.end_date < today]

        for interval in intervals:
            activities = RegisterActivity.objects.filter(
                interval=interval).all()
            activity_names = [
                activity.activity.name for activity in activities]
            unique_activity_names = list(set(activity_names))
            serialized_intervals.append({
                'interval_id': interval.id,
                'start_date': interval.start_date,
                'end_date': interval.end_date,
                'activities': unique_activity_names
            })

        return serialized_intervals

    def get_avg_corporal_meditions(self, competence):
        """Calculate average corporal meditions for the given competence."""
        meditions = CorporalMeditions.objects.filter(
            profile__user__group_participation__enterprise=competence.enterprise).all()
        total_weight = 0
        total_height = 0
        total_fat = 0
        count = meditions.count()

        for medition in meditions:
            total_weight += medition.weight
            total_height += medition.height
            total_fat += medition.fat

        if count > 0:
            avg_weight = round(total_weight / count, 1)
            avg_height = round(total_height / count, 1)
            avg_fat = round(total_fat / count, 1)
        else:
            avg_weight = 0
            avg_height = 0
            avg_fat = 0

        return {
            'weight': avg_weight,
            'height': avg_height,
            'fat': avg_fat
        }

    def get_stats(self, competence):
        """Get statistics for the given competence."""
        intervals = Interval.objects.filter(
            competence=competence).order_by('-end_date').all()
        active_interval = self._get_active_interval(intervals)
        if active_interval:
            intervals = [active_interval] + \
                [interval for interval in intervals if interval !=
                    active_interval and interval.end_date <= date.today()]

        team_data = self._initialize_team_data(intervals)

        for interval in intervals:
            self._process_interval(interval, team_data)

        ranking, my_team = self._generate_ranking(team_data)
        current_interval_data = self._get_current_interval_data(
            active_interval)
        historical_data = self._get_historical_data(intervals)

        return {
            'teams': ranking,
            'my_team': my_team,
            'current_interval_data': current_interval_data,
            'historical_data': historical_data
        }

    def get_days_remaining_competence(self, competence):
        """Get days remaining for the competence to end."""
        today = date.today()
        end_date = competence.end_date
        return (end_date - today).days if end_date >= today else 0

    def get_days_remaining_interval(self, competence):
        """Get days remaining for the current interval to end."""
        active_interval = self._get_active_interval(
            Interval.objects.filter(competence=competence).order_by('-end_date').all())
        if active_interval:
            today = date.today()
            end_date = active_interval.end_date
            return (end_date - today).days if end_date >= today else 0
        return 0

    def _initialize_team_data(self, intervals):
        return {
            'total_activities': 0,
            'team_points': {},
            'team_participants': {},
            'team_interval_points': {},
            'interval_activity_count': {},
            'interval_completed_activity_count': {},
            'interval_incomplete_activity_count': {},
            'team_medition_avg': {}
        }

    def _get_active_interval(self, intervals):
        today = date.today()
        for interval in intervals:
            if interval.start_date <= today <= interval.end_date:
                return interval
        return None

    def _process_interval(self, interval, team_data):
        activities = RegisterActivity.objects.filter(
            interval=interval).all()
        team_data['interval_activity_count'][interval.id] = activities.count()
        team_data['interval_completed_activity_count'][interval.id] = activities.filter(
            is_completed=True).count()
        team_data['interval_incomplete_activity_count'][interval.id] = activities.filter(
            is_completed=False).count()

        for activity in activities:
            team_id = activity.user.group_participation.id
            team_name = activity.user.group_participation.name
            if team_id not in team_data['team_points']:
                team_data['team_points'][team_id] = 0
                team_data['team_participants'][team_id] = set()
                team_data['team_interval_points'][team_id] = {}
                team_data['team_medition_avg'][team_id] = {
                    'weight': [],
                    'height': [],
                    'fat': []
                }

            if activity.is_active:
                team_data['team_participants'][team_id].add(
                    activity.user.id)

            if interval.id not in team_data['team_interval_points'][team_id]:
                team_data['team_interval_points'][team_id][interval.id] = 0

            if activity.is_completed:
                team_data['team_points'][team_id] += activity.activity.points
                team_data['team_interval_points'][team_id][interval.id] += activity.activity.points

            # Add corporal medition to team data
            meditions = CorporalMeditions.objects.filter(
                profile=Profile.objects.filter(user=activity.user).last()).all()
            for medition in meditions:
                team_data['team_medition_avg'][team_id]['weight'].append(
                    medition.weight)
                team_data['team_medition_avg'][team_id]['height'].append(
                    medition.height)
                team_data['team_medition_avg'][team_id]['fat'].append(
                    medition.fat)

            team_data['total_activities'] += 1

    def _generate_ranking(self, team_data):
        ranking = []
        my_team = None
        for team_id in team_data['team_points']:
            interval_points, total = self._calculate_interval_points(
                team_id, team_data)
            medition_avg = self._calculate_medition_avg(
                team_data['team_medition_avg'][team_id])
            team_info = {
                'team_id': team_id,
                'name': Group.objects.get(id=team_id).name,
                'points': total,
                'intervals': interval_points,
                'medition_avg': medition_avg
            }

            if team_id == self.context['request'].user.group_participation.id:
                my_team = team_info

            ranking.append(team_info)

        ranking.sort(key=lambda x: x['points'], reverse=True)
        for position, team in enumerate(ranking, start=1):
            team['position'] = position
            if team['team_id'] == self.context['request'].user.group_participation.id:
                my_team['position'] = position

        return ranking, my_team

    def _calculate_interval_points(self, team_id, team_data):
        interval_points = []
        total = 0
        for interval_id, interval_points_sum in team_data['team_interval_points'][team_id].items():
            interval_activities = RegisterActivity.objects.filter(
                interval_id=interval_id, user__group_participation_id=team_id).all()
            interval_participants = set(
                activity.user.id for activity in interval_activities if activity.is_active)
            interval_obj = Interval.objects.get(id=interval_id)
            points = interval_points_sum / \
                len(interval_participants) if interval_participants else 0
            interval_points.append({
                'interval_id': interval_id,
                'start_date': interval_obj.start_date,
                'end_date': interval_obj.end_date,
                'points': points,
                'participants_count': len(interval_participants),
                'completed_activities': team_data['interval_completed_activity_count'][interval_id],
                'incomplete_activities': team_data['interval_incomplete_activity_count'][interval_id],
                'activities': RegisterActivitySerializer(interval_activities, many=True).data
            })
            total += points
        return interval_points, total

    def _calculate_medition_avg(self, meditions):
        if not meditions['weight'] or not meditions['height'] or not meditions['fat']:
            return {'weight': 0, 'height': 0, 'fat': 0}
        return {
            'weight': sum(meditions['weight']) / len(meditions['weight']),
            'height': sum(meditions['height']) / len(meditions['height']),
            'fat': sum(meditions['fat']) / len(meditions['fat'])
        }

    def _get_current_interval_data(self, active_interval):
        if not active_interval:
            return None

        user = self.context['request'].user
        user_activities = RegisterActivity.objects.filter(
            interval=active_interval, user=user).all()
        team_activities = RegisterActivity.objects.filter(
            interval=active_interval, user__group_participation=user.group_participation).all()

        team_activities_by_user = {}
        for activity in team_activities:
            user_email = activity.user.email
            if user_email not in team_activities_by_user:
                team_activities_by_user[user_email] = []
            team_activities_by_user[user_email].append({
                'activity': activity.activity.name,
                'is_completed': activity.is_completed,
                'is_load': activity.is_load,
                'start_date': activity.interval.start_date,
                'end_date': activity.interval.end_date
            })

        return {
            'start_date': active_interval.start_date,
            'end_date': active_interval.end_date,
            'user': RegisterActivitySerializer(user_activities, many=True).data,
            'my_group': team_activities_by_user
        }

    def _get_historical_data(self, intervals):
        historical_data = []
        for interval in intervals:
            interval_data = self._get_historical_interval_data(
                interval)
            if interval_data:
                historical_data.append({
                    'interval_id': interval.id,
                    'start_date': interval.start_date,
                    'end_date': interval.end_date,
                    'data': interval_data,

                })
        return historical_data

    def _get_historical_interval_data(self, interval):
        user = self.context['request'].user
        user_activities = RegisterActivity.objects.filter(
            interval=interval, user=user).all()
        team_activities = RegisterActivity.objects.filter(
            interval=interval, user__group_participation=user.group_participation).all()

        user_data = {
            'is_active': user_activities.filter(is_active=True).count(),
            'is_completed': user_activities.filter(is_completed=True).count(),
            'activities': RegisterActivitySerializer(user_activities, many=True).data
        }

        team_data = {
            'is_active': team_activities.filter(is_active=True).count(),
            'is_completed': team_activities.filter(is_completed=True).count(),
            'activities': RegisterActivitySerializer(team_activities, many=True).data
        }

        return {
            'user': user_data,
            'my_team': team_data
        }

    class Meta:
        model = Competence
        fields = ('id', 'name', 'description', 'start_date',
                  'end_date', 'interval_quantity', 'days_for_interval', 'stats', 'days_remaining_competence', 'days_remaining_interval', 'avg_corporal_meditions', 'intervals_to_back')


class EnterpriseSerializer(serializers.ModelSerializer):
    last_competence = serializers.SerializerMethodField('get_competence')

    def get_competence(self, enterprise):
        request = self.context['request']
        competences = Competence.objects.filter(
            enterprise=enterprise).last()
        serializer = CompetenceSelectSerializer(
            competences, many=False, context={'request': request})
        return serializer.data

    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'last_competence')


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

class CompetenceRankingSerializer(serializers.ModelSerializer):
    ranking = serializers.SerializerMethodField('get_ranking')

    def get_ranking(self, competence):
        intervals = Interval.objects.filter(
            competence=competence).order_by('start_date').all()
        team_points = {}
        interval_data = {}

        # Inicializa interval_data con todos los intervalos para cada equipo
        for interval in intervals:
            teams = Group.objects.all()
            for team in teams:
                team_id = team.id
                if team_id not in interval_data:
                    interval_data[team_id] = {}
                if interval.id not in interval_data[team_id]:
                    interval_data[team_id][interval.id] = {
                        'unique_participants': set(),
                        'completed_activities_count': 0,
                        'total_points': 0,
                        'is_load_activities_count': 0
                    }

        # Rellena interval_data con las actividades filtradas por equipo e intervalo
        for interval in intervals:
            register_activities = RegisterActivity.objects.filter(
                interval=interval).all()
            for register_activity in register_activities:
                team_id = register_activity.user.group_participation.id
                interval_data[team_id][interval.id]['unique_participants'].add(register_activity.user.id)
                if register_activity.is_completed:
                    interval_data[team_id][interval.id]['completed_activities_count'] += 1
                    interval_data[team_id][interval.id]['total_points'] += register_activity.activity.points
                if register_activity.is_load:
                    interval_data[team_id][interval.id]['is_load_activities_count'] += 1

        # Calcula puntos promedio por intervalo
        for team_id in interval_data:
            for interval_id in interval_data[team_id]:
                interval = interval_data[team_id][interval_id]
                if interval['unique_participants']:
                    interval['average_points'] = interval['total_points'] / len(interval['unique_participants'])
                else:
                    interval['average_points'] = 0

        # Suma puntos promedio para el ranking
        for team_id in interval_data:
            team_points[team_id] = sum(interval['average_points'] for interval in interval_data[team_id].values())

        ranking = sorted(team_points.items(), key=lambda x: x[1], reverse=True)
        ranked_teams = []
        for position, (team_id, points) in enumerate(ranking, start=1):
            team = Group.objects.get(id=team_id)
            ranked_teams.append({
                'team_id': team_id,
                'team_name': team.name,
                'points': points,
                'position': position
            })

        return {'teams': ranked_teams}

    class Meta:
        model = Competence
        fields = ('name','ranking',)

class CompetenceRetrieveSerializer(serializers.ModelSerializer):
    ranking = serializers.SerializerMethodField('get_ranking')

    def get_ranking(self, competence):
        request = self.context.get('request')
        intervals = Interval.objects.filter(
            competence=competence).order_by('start_date').all()
        team_points = {}
        interval_data = {}

        # Inicializa interval_data con todos los intervalos para cada equipo
        for interval in intervals:
            teams = Group.objects.all()
            for team in teams:
                team_id = team.id
                if team_id not in interval_data:
                    interval_data[team_id] = {}
                if interval.id not in interval_data[team_id]:
                    interval_data[team_id][interval.id] = {
                        'interval_id': interval.id,
                        'start_date': interval.start_date,
                        'end_date': interval.end_date,
                        'activities': {},
                        'unique_participants': set(),
                        'completed_activities_count': 0,
                        'total_points': 0,
                        'is_load_activities_count': 0
                    }

        # Rellena interval_data con las actividades filtradas por equipo e intervalo
        for interval in intervals:
            register_activities = RegisterActivity.objects.filter(
                interval=interval).all()
            for register_activity in register_activities:
                team_id = register_activity.user.group_participation.id
                activity_name = register_activity.activity.name
                if activity_name not in interval_data[team_id][interval.id]['activities']:
                    interval_data[team_id][interval.id]['activities'][activity_name] = []

                interval_data[team_id][interval.id]['activities'][activity_name].append({
                    'user_email': register_activity.user.email,
                    'is_completed': register_activity.is_completed,
                    'is_load': register_activity.is_load,
                    'file': request.build_absolute_uri(register_activity.file.url) if register_activity.file else None,
                    'register_activity_id': register_activity.id,
                })
                interval_data[team_id][interval.id]['unique_participants'].add(register_activity.user.id)
                if register_activity.is_completed:
                    interval_data[team_id][interval.id]['completed_activities_count'] += 1
                    interval_data[team_id][interval.id]['total_points'] += register_activity.activity.points
                if register_activity.is_load:
                    interval_data[team_id][interval.id]['is_load_activities_count'] += 1

        # Calcula usuarios únicos por equipo
        team_users = {team_id: len(participants['unique_participants']) for team_id, intervals in interval_data.items() for interval_id, participants in intervals.items()}

        # Calcula puntos promedio por intervalo
        for team_id in interval_data:
            for interval_id in interval_data[team_id]:
                interval = interval_data[team_id][interval_id]
                if interval['unique_participants']:
                    interval['average_points'] = interval['total_points'] / len(interval['unique_participants'])
                else:
                    interval['average_points'] = 0

        # Suma puntos promedio para el ranking
        for team_id in interval_data:
            team_points[team_id] = sum(interval['average_points'] for interval in interval_data[team_id].values())

        ranking = sorted(team_points.items(), key=lambda x: x[1], reverse=True)
        ranked_teams = []
        for position, (team_id, points) in enumerate(ranking, start=1):
            team = Group.objects.get(id=team_id)
            intervals_list = list(interval_data[team_id].values())
            intervals_list.sort(key=lambda x: x['start_date'])
            ranked_teams.append({
                'team_id': team_id,
                'team_name': team.name,
                'points': points,
                'position': position,
                'intervals': [
                    {
                        'interval_id': interval['interval_id'],
                        'start_date': interval['start_date'].strftime('%d-%m'),
                        'end_date': interval['end_date'].strftime('%d-%m'),
                        'average_points': interval['average_points'],
                        'completed_activities_count': interval['completed_activities_count'],
                        'is_load_activities_count': interval['is_load_activities_count'],
                        'activities': [
                            {
                                'activity_name': activity_name,
                                'registers': activity_registers
                            }
                            for activity_name, activity_registers in interval['activities'].items()
                        ]
                    }
                    for interval in intervals_list
                ]
            })

        return {'teams': ranked_teams}

    class Meta:
        model = Competence
        fields = '__all__'
        depth = 2