from django.db import models
from api.utils.models import ModelApi

class Competence(ModelApi):
    name = models.CharField(max_length=1200, verbose_name='nombre')
    description = models.TextField(
        max_length=1200, blank=True, null=True, verbose_name='descripcion')

    class Meta:
        verbose_name = 'Competencia'
        verbose_name_plural = 'Competencias'

    def __str__(self):
        return str(self.name)


class Enterprise(ModelApi):
    name = models.CharField(max_length=1200, verbose_name='nombre')
    description = models.TextField(
        max_length=1200, blank=True, null=True, verbose_name='descripcion')
    address = models.CharField(
        max_length=1200, blank=True, null=True, verbose_name='direccion')
    phone = models.CharField(max_length=1200, blank=True,
                             null=True, verbose_name='telefono')
    email = models.EmailField(
        max_length=1200, blank=True, null=True, verbose_name='correo')
    points = models.IntegerField(default=0, verbose_name='puntos')
    competences = models.ForeignKey(Competence, on_delete=models.CASCADE, verbose_name='competencia')

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return str(self.name)


class Group(ModelApi):
    name = models.CharField(max_length=1200, verbose_name='nombre')
    description = models.TextField(
        max_length=1200, blank=True, null=True, verbose_name='descripcion')
    enterprise = models.ForeignKey(
        Enterprise, on_delete=models.CASCADE, verbose_name='empresa')
    points = models.IntegerField(default=0, verbose_name='puntos')

    class Meta:
        verbose_name = 'Equipos(grupos)'
        verbose_name_plural = 'Equipo(grupos)'

    def __str__(self):
        if self.enterprise.name and self.name:
            return f"{self.enterprise.name} - {self.name}"
        elif self.name:
            return self.name
        else:
            return ""
