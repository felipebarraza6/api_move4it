from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from api.users.models import User, Profile, CorporalMeditions, SportActivity, PreviousIllnesse
from import_export.admin import ExportActionMixin


class UserAdm(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        'username',
        "points",
        'group_participation',
        'email',
        'first_name',
        'last_name',
        'identification_number',
        'type_user',
        "gender",
    )
    search_fields = ('email', 'identification_number')
    list_filter = ('type_user', "group_participation", "gender",)
    ordering = ('-created',)

    def save_model(self, request, obj, form, change):
        if obj.password == "pbkdf2" + "*":
            obj.password = obj.password
        else:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdm)
admin.site.register(SportActivity)
admin.site.register(PreviousIllnesse)

@admin.register(Profile)
class ProfileMedicionesAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('user', 'wellnes_goal', 'target_weight', 'target_fat', 'sports_frequancy')
    search_fields = ('user', )
    list_filter = ( 'target_weight', 'target_fat', 'sports_frequancy', "sports_activities", "previous_illnesses")
    ordering = ('-created',)


@admin.register(CorporalMeditions)
class CorporalMeditionsAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('profile', 'height', 'weight', 'fat')
    search_fields = ('profile', )
    list_filter = ("created", "height", "weight", "fat")
    ordering = ('-created',)
    
