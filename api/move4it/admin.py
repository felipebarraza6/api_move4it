
from import_export.admin import ExportActionMixin
from django.contrib import admin
from django.utils.html import format_html
from datetime import date, timedelta
from api.move4it.models import (Blog, Enterprise, Group, Activity,
                                ActivityCategory, TypeMedition, RegisterActivity, Competence,
                                FileRegisterActivity, Interval)
from django.conf.locale.es import formats as es_formats

es_formats.DATE_FORMAT = "d/m/Y"
es_formats.DATETIME_FORMAT = "d/m/Y H:i"

admin.site.register(Blog)


@admin.register(Interval)
class IntervalAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('id', 'competence', 'get_enterprise', "set_status", 'start_date',
                    'end_date', 'get_activities_count')
    search_fields = ('name', )
    list_filter = ('competence', 'start_date', 'end_date')
    date_hierarchy = 'created'

    def set_status(self, obj):
        """set status"""
        today = date.today()
        if obj.end_date < today:
            return "Finalizado"
        elif obj.start_date <= today and obj.end_date >= today:
            return "Activo"
        else:
            return "Pendiente"
    set_status.short_description = 'Estado'

    def get_enterprise(self, obj):
        """get enterprise"""
        return obj.competence.enterprise.name

    def get_activities_count(self, obj):
        """get activities count"""
        return obj.activities.count()

    get_enterprise.short_description = 'Empresa'
    get_activities_count.short_description = 'Cantidad de Actividades'


@admin.register(Enterprise)
class EnterpriseAdmin(ExportActionMixin, admin.ModelAdmin):
    """Enterprise Admin"""

    def get_equipment_count(self, obj):
        """get count equipment"""
        return obj.group_set.count()

    get_equipment_count.short_description = 'Cantidad de Equipos'

    def get_user_count(self, obj):
        """get count user"""
        groups = obj.group_set.all()
        user_count = sum(group.user_set.count() for group in groups)
        return user_count

    get_user_count.short_description = 'Participantes'

    list_display = ('name', "points", 'email', 'phone', 'address',
                    'get_equipment_count', 'get_user_count')
    date_hierarchy = 'created'


@admin.register(Group)
class GroupAdmin(ExportActionMixin, admin.ModelAdmin):

    list_filter = ('enterprise', )

    def get_equipment_count(self, obj):
        return obj.user_set.count()

    def get_leader_name(self, obj):
        leader = obj.user_set.filter(is_leader=True).first()
        if leader:
            return f"{leader.first_name} {leader.last_name} / {leader.email}"
        return None

    get_equipment_count.short_description = 'Participantes'
    get_leader_name.short_description = 'Líder de Grupo'

    list_display = ('name', "enterprise", 'get_equipment_count',
                    'get_leader_name', "points")


@admin.register(Activity)
class ActivityAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('name', 'category', "type_medition",
                    'points', 'global_points', "is_global")
    search_fields = ('name', )
    list_filter = ('category', 'type_medition',
                   'is_global', "points", "global_points")
    date_hierarchy = 'created'


@admin.register(ActivityCategory)
class ActivityCategoryAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(TypeMedition)
class TypeMeditionAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('name', )


@admin.register(FileRegisterActivity)
class FileRegisterActivityAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('register_activity', 'file', "user")
    search_fields = ('register_activity', )
    list_filter = ("user", )
    date_hierarchy = 'created'
    date_hierarchy = 'created'


@admin.register(RegisterActivity)
class RegisterActivityAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('activity', "get_users", "get_enterprises", "get_groups", 'set_status', "start_date_time", "finish_date_time",
                    "is_completed", "is_load")

    list_filter = ('interval__competence__name', 'activity', 'users', 'interval',
                   'start_date_time', 'finish_date_time')
    search_fields = ('activity', )
    date_hierarchy = 'created'

    def set_status(self, obj):
        """set status"""
        today = date.today()
        if obj.finish_date_time.date() < today:
            return "Finalizado"
        elif obj.start_date_time.date() <= today and obj.finish_date_time.date() >= today:
            return "Activo"
        else:
            return "Pendiente"
    set_status.short_description = 'Estado'

    def get_users(self, obj):
        """get users"""
        return format_html("<br>".join([p.email for p in obj.users.all()]))

    def get_groups(self, obj):
        """get groups"""
        return format_html("<br>".join([p.group_participation.name for p in obj.users.all()]))

    def get_enterprises(self, obj):
        """get enterprises"""
        return format_html("<br>".join([p.group_participation.enterprise.name for p in obj.users.all()]))

    get_users.short_description = 'Usuario'  # Nombre del campo en el admin
    get_groups.short_description = 'Grupo'
    get_enterprises.short_description = 'Empresa'


@admin.register(Competence)
class CompetenceAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('name',  "enterprise", "set_status", "start_date", 'end_date', "total_duration", "get_actual_invertal",
                    "interval_quantity", "days_for_interval", "get_quantity_groups", "get_quantity_users")

    def set_status(self, obj):
        """set status"""
        today = date.today()
        if obj.end_date < today:
            return "Finalizado"
        elif obj.start_date <= today and obj.end_date >= today:
            return "Activo"
        else:
            return "Pendiente"
    set_status.short_description = 'Estado'

    def total_duration(self, obj):
        """Calculate the total duration in days"""
        duration = (obj.end_date - obj.start_date) + timedelta(days=1)
        total_days = duration.days
        return f"{total_days} días"

    total_duration.short_description = 'Duración total'

    def get_quantity_groups(self, obj):
        """get quantity groups"""
        return Group.objects.filter(enterprise=obj.enterprise).count()
    get_quantity_groups.short_description = 'Cantidad de Grupos'

    def get_quantity_users(self, obj):
        """get quantity users"""
        groups = Group.objects.filter(enterprise=obj.enterprise)
        user_count = sum(group.user_set.count() for group in groups)
        return user_count
    get_quantity_users.short_description = 'Cantidad de Participantes'

    def get_actual_invertal(self, obj):
        """get actual interval"""
        today = date.today()
        intervals = obj.interval_set.filter(
            start_date__lte=today, end_date__gte=today)
        interval = intervals.first()
        if interval:
            return f"{interval.start_date.strftime('%Y-%m-%d')} \n {interval.end_date.strftime('%Y-%m-%d')}"
        return None

    get_actual_invertal.short_description = 'Intervalo Actual'

    search_fields = ('name', )
    list_filter = ('enterprise', 'start_date', 'end_date')
    date_hierarchy = 'created'
