"""Register activities model."""
from django.db import models
from api.utils.models import ModelApi
from .activities import Activity
from .enterprises import Enterprise, Group, Interval


class RegisterActivity(ModelApi):
    """Register activity model."""
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, verbose_name='actividad')
    interval = models.ForeignKey(
        Interval, on_delete=models.CASCADE, verbose_name='intervalo', blank=True, null=True)

    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, verbose_name='usuario')

    duration = models.IntegerField(
        default=0, verbose_name='duración', blank=True, null=True)

    observation = models.TextField(
        max_length=1200, blank=True, null=True, verbose_name='observación(administrador')
    location = models.CharField(
        max_length=1200, blank=True, null=True, verbose_name='ubicación(lat/long)')
    value = models.FloatField(verbose_name='valor', blank=True, null=True)

    is_active = models.BooleanField(default=True, verbose_name='esa activo')
    is_completed = models.BooleanField(
        default=False, verbose_name='esta completado')
    is_load = models.BooleanField(
        default=False, verbose_name='cargo evidencia')

    class Meta:
        """Register activity model."""
        verbose_name = 'Actividades - Registro'
        verbose_name_plural = 'Actividades - Registros'

    def __str__(self):
        return str(self.activity)


class FileRegisterActivity(ModelApi):
    register_activity = models.ForeignKey(
        RegisterActivity, on_delete=models.CASCADE, verbose_name='registro de actividad')
    file = models.FileField(upload_to='activities/',
                            blank=True, null=True, verbose_name='archivo')
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name='usuario')
    message = models.TextField(
        max_length=1200, blank=True, null=True, verbose_name='mensaje')
    observation = models.TextField(
        max_length=1200, blank=True, null=True, verbose_name='observación(administrador')

    class Meta:
        verbose_name = 'Actividades - Registro - Archivo'
        verbose_name_plural = 'Actividades - Registros - Archivos'

    def __str__(self):
        return str(self.register_activity)
