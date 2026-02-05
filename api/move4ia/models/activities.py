"""Activities models."""
from django.db import models
from api.utils.models import ModelApi


class ActivityCategory(ModelApi):
    """ActivityCategory model."""
    name = models.CharField(max_length=1200, verbose_name='nombre')
    description = models.TextField(
        max_length=1200, blank=True, null=True, verbose_name='descripción')

    class Meta:
        """ActivityCategory Meta definition."""
        verbose_name = 'Actividades - Categoria'
        verbose_name_plural = 'Actividades - Categorias'

    def __str__(self):
        return str(self.name)


class TypeMedition(ModelApi):
    """TypeMedition model."""
    name = models.CharField(max_length=1200, verbose_name='nombre')
    image_on = models.ImageField(
        upload_to='activities/', blank=True, null=True, verbose_name='imagen')
    image_off = models.ImageField(
        upload_to='activities/', blank=True, null=True, verbose_name='imagen')
    achievement_1 = models.IntegerField(default=0, verbose_name='logro 1')
    achievement_2 = models.IntegerField(default=0, verbose_name='logro 2')
    achievement_3 = models.IntegerField(default=0, verbose_name='logro 3')
    achievement_4 = models.IntegerField(default=0, verbose_name='logro 4')
    achievement_5 = models.IntegerField(default=0, verbose_name='logro 5')
    achievement_6 = models.IntegerField(default=0, verbose_name='logro 6')
    achievement_7 = models.IntegerField(default=0, verbose_name='logro 7')
    achievement_8 = models.IntegerField(default=0, verbose_name='logro 8')
    achievement_9 = models.IntegerField(default=0, verbose_name='logro 9')
    achievement_10 = models.IntegerField(default=0, verbose_name='logro 10')

    class Meta:
        """Meta definition for TypeMedition."""
        verbose_name = 'Actividades - Tipo de medición'
        verbose_name_plural = 'Actividades - Tipos de medición'

    def __str__(self):
        return str(self.name)


class Activity(ModelApi):
    """Activity model."""
    name = models.CharField(max_length=1200, verbose_name='nombre')
    image = models.ImageField(upload_to='activities/',
                              blank=True, null=True, verbose_name='imagen')
    category = models.ForeignKey(
        ActivityCategory, on_delete=models.CASCADE, verbose_name='categoría')
    type_medition = models.ForeignKey(
        TypeMedition, on_delete=models.CASCADE,
        verbose_name='tipo de medición', blank=True, null=True)
    value = models.FloatField(verbose_name='valor', blank=True, null=True)
    calories_burned = models.IntegerField(
        default=0, verbose_name='kcal quemadas')

    description = models.TextField(
        max_length=1200, blank=True, null=True, verbose_name='descripción')
    points = models.IntegerField(default=0, verbose_name='puntos')
    duration = models.IntegerField(default=0, verbose_name='duración')
    is_active = models.BooleanField(default=True, verbose_name='esta activo')

    CHOICES_STATS = (("INCREMENTAL", "incremental"),
                     ("PORCENTAJE", "porcentaje"))

    type_stats = models.CharField(
        max_length=1200, verbose_name='tipo de estadísticas', blank=True, null=True,
        choices=CHOICES_STATS
    )

    class Meta:
        """Meta definition for Activity."""
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

    def __str__(self):
        return str(self.name)
