
from import_export.admin import ExportActionMixin
from django.contrib import admin
from django.utils.html import format_html
from api.move4it.models import (Blog, Enterprise, Group, Activity,
                                ActivityCategory, TypeMedition, RegisterActivity, Competence,
                                FileRegisterActivity, Interval)
admin.site.register(Blog)


@admin.register(Interval)
class IntervalAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('id', 'start_date', 'end_date',)
    search_fields = ('name', )
    list_filter = ('created', )
    date_hierarchy = 'created'


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
    list_display = ('activity', "get_users", "get_groups",
                    "get_enterprises", 'observation', "is_active")
    list_filter = ('activity', 'users', 'groups', 'enterprises', 'activity',)
    search_fields = ('activity', )
    date_hierarchy = 'created'

    def get_users(self, obj):
        """get users"""
        return format_html("<br>".join([p.email for p in obj.users.all()]))

    def get_groups(self, obj):
        """get groups"""
        return format_html("<br>".join([p.name for p in obj.groups.all()]))

    def get_enterprises(self, obj):
        """get enterprises"""
        return format_html("<br>".join([p.name for p in obj.enterprises.all()]))

    get_users.short_description = 'Usuarios'  # Nombre del campo en el admin
    get_groups.short_description = 'Grupos'
    get_enterprises.short_description = 'Empresas'


@admin.register(Competence)
class CompetenceAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', )
    list_filter = ('created', )
    date_hierarchy = 'created'
