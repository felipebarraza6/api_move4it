from django.db import models

from api.utils.models import ModelApi
from .users import User


class SportActivity(ModelApi):
    name = models.CharField(max_length=1200, verbose_name='nombre')

    class Meta:
        verbose_name = 'Deporte'
        verbose_name_plural = 'Deportes'

    def __str__(self):
        return str(self.name)


class PreviousIllnesse(ModelApi):
    name = models.CharField(max_length=1200, verbose_name='nombre')

    class Meta:
        verbose_name = 'Enfermedad previa'
        verbose_name_plural = 'Enfermedades previas'

    def __str__(self):
        return str(self.name)


class Profile(ModelApi):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sports_activities = models.ManyToManyField(SportActivity, verbose_name='Actividades', blank=True)
    wellnes_goal = models.TextField(
        verbose_name='Objetivo de bienestar', blank=True, null=True)
    date_of_birth = models.DateField(
        verbose_name='Fecha de nacimiento', blank=True, null=True)
    bio = models.TextField(verbose_name='Biografía', blank=True, null=True)
    target_weight = models.FloatField(
        verbose_name='Peso objetivo', blank=True, null=True)
    target_fat = models.FloatField(verbose_name='Grasa objetivo', blank=True, null=True)
    sports_frequancy= models.IntegerField( verbose_name='Frecuencia de deporte', blank=True, null=True)
    previous_illnesses = models.ManyToManyField(PreviousIllnesse, verbose_name='Enfermedades previas', blank=True)
    sports_consulting = models.TextField(max_length=1200, verbose_name='Consulta deportiva', blank=True, null=True)
    nutritional_advice = models.TextField(max_length=1200, verbose_name='Consulta nutricional', blank=True, null=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'


    def __str__(self):
        return str(self.user)


class CorporalMeditions(ModelApi):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    height = models.DecimalField(verbose_name='Altura', max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.FloatField(verbose_name='Peso', blank=True, null=True)
    fat = models.FloatField(verbose_name='Grasa', blank=True, null=True)

    class Meta:
        verbose_name = 'Medicion'
        verbose_name_plural = 'Mediciones'

    def __str__(self):
        return str(self.profile)

