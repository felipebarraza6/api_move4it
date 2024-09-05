"""Models Enterprise module gestion."""
from django.db import models
from api.utils.models import ModelApi
from .activities import Activity


class Enterprise(ModelApi):
    """Ennterprise Model."""
    name = models.CharField(max_length=1200, verbose_name='nombre')
    description = models.TextField(
        max_length=1200, blank=True, null=True, verbose_name='descripción')
    address = models.CharField(
        max_length=1200, blank=True, null=True, verbose_name='dirección')
    phone = models.CharField(max_length=1200, blank=True,
                             null=True, verbose_name='Telefono')
    email = models.EmailField(
        max_length=1200, blank=True, null=True, verbose_name='correo')
    points = models.IntegerField(default=0, verbose_name='puntos')

    class Meta:
        """Meta Enterprise model."""
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return str(self.name)


class Group(ModelApi):
    """Grupo model."""
    name = models.CharField(max_length=1200, verbose_name='nombre')
    description = models.TextField(
        max_length=1200, blank=True, null=True, verbose_name='descripción')
    enterprise = models.ForeignKey(
        Enterprise, on_delete=models.CASCADE, verbose_name='empresa')
    points = models.IntegerField(default=0, verbose_name='puntos')

    class Meta:
        "meta group model."
        verbose_name = 'Equipos(grupos)'
        verbose_name_plural = 'Equipo(grupos)'

    def __str__(self):
        if self.enterprise.name and self.name:
            return f"{self.enterprise.name} - {self.name}"
        elif self.name:
            return self.name
        else:
            return ""


class Competence(ModelApi):
    """Competence model."""
    enterprise = models.ForeignKey(
        Enterprise, on_delete=models.CASCADE, verbose_name='empresa')
    name = models.CharField(max_length=1200, verbose_name='nombre')
    description = models.TextField(
        max_length=1200, blank=True, null=True, verbose_name='descripción')
    start_date = models.DateField(verbose_name='fecha de inicio')
    end_date = models.DateField(
        blank=True, null=True, verbose_name='fecha de fin')
    interval_quantity = models.IntegerField(
        default=0, verbose_name='intervalo')
    days_for_interval = models.IntegerField(
        default=0, verbose_name='Dias por intervalo')
    is_finished = models.BooleanField(default=False, verbose_name='finalizado')

    class Meta:
        """Meta competence model."""
        verbose_name = 'Competencia'
        verbose_name_plural = 'Competencias'

    def __str__(self):
        return str(self.name)


class Interval(ModelApi):
    """Interval model."""
    competence = models.ForeignKey(
        Competence, on_delete=models.CASCADE, verbose_name='competencia')
    start_date = models.DateField(
        blank=True, null=True, verbose_name='fecha de inicio')
    end_date = models.DateField(
        blank=True, null=True, verbose_name='fecha de fin')
    activities = models.ManyToManyField(
        Activity, verbose_name='actividades')
    is_finished = models.BooleanField(default=False, verbose_name='finalizado')
    generate_assignments = models.BooleanField(
        default=False, verbose_name='crear asignaciones')

    class Meta:
        """Meta interval model."""
        verbose_name = 'Intervalo'
        verbose_name_plural = 'Intervalos'

    def __str__(self):
        return str(("C: {} / F.I:{}").format(self.competence, self.start_date, self.end_date))
