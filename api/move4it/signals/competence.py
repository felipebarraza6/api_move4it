from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from datetime import timedelta
# Asegúrate de importar tus modelos
from api.move4it.models import Competence, Interval, RegisterActivity
from api.users.models import User


@receiver(post_save, sender=Competence)
def create_intervals(sender, instance, created, **kwargs):
    if created:
        # Desconectar temporalmente la señal para evitar recursión
        post_save.disconnect(create_intervals, sender=Competence)
        try:
            quantity_intervals = instance.interval_quantity
            days_for_interval = instance.days_for_interval
            start_date = instance.start_date
            # Calcular la fecha de fin de cada intervalo
            intervals = []
            for _ in range(quantity_intervals):
                end_date = start_date + timedelta(days=days_for_interval)
                interval = Interval(competence=instance,
                                    start_date=start_date, end_date=end_date)
                intervals.append(interval)
                start_date = end_date + timedelta(days=1)

            # Guardar los intervalos en la base de datos
            Interval.objects.bulk_create(intervals)
            # Asignar la fecha final del último intervalo como instance.end_date
            instance.end_date = intervals[-1].end_date
            # Guardar la instancia si se ha modificado
            instance.save()
        finally:
            # Volver a conectar la señal
            post_save.connect(create_intervals, sender=Competence)


@receiver(post_save, sender=Interval)
def create_assignments(sender, instance, created, **kwargs):
    # Desconectar temporalmente la señal para evitar recursión
    post_save.disconnect(create_assignments, sender=Interval)

    try:
        # Obtener las actividades de la competencia
        activities = instance.activities.all()
        # Asignar las actividades al intervalo
        # Obtener los usuarios de la competencia
        users = User.objects.filter(
            group_participation__enterprise=instance.competence.enterprise)
        competence = instance.competence
        if created:
            Competence.objects.filter(id=competence.id).update(
                interval_quantity=competence.interval_quantity+1, end_date=competence.end_date + timedelta(days=competence.days_for_interval))
            instance.start_date = Interval.objects.filter(
                competence=competence.id).order_by('end_date').last().end_date
            instance.end_date = instance.start_date + \
                timedelta(days=competence.days_for_interval)
            instance.save()

        if instance.generate_assignments:
            for user in users:
                for activity in activities:
                    register_activity = RegisterActivity.objects.create(
                        activity=activity,
                        start_date_time=instance.start_date,
                        finish_date_time=instance.end_date
                    )
                    register_activity.users.set([user])
            instance.generate_assignments = False
            instance.save()
    finally:
        # Volver a conectar la señal
        post_save.connect(create_assignments, sender=Interval)
