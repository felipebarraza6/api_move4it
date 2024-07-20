from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from api.move4it.models import RegisterActivity, Group, Enterprise  # Asegúrate de importar tus modelos
from api.users.models import User

@receiver(post_save, sender=RegisterActivity)
def update_user(sender, instance, created, **kwargs):
    if not created:
        # Desconectar temporalmente la señal para evitar recursión
        post_save.disconnect(update_user, sender=RegisterActivity)

        try:
            instance.is_active = False
            if instance.is_user and instance.is_completed:
                for user in instance.users.all():
                    User.objects.filter(id=user.id).update(points=user.points + instance.activity.points)

            if instance.is_group and instance.is_completed:
                for group in instance.groups.all():
                    Group.objects.filter(id=group.id).update(points=group.points + instance.activity.global_points)

            if instance.is_global and instance.is_completed:
                for enterprise in instance.enterprises.all():
                    Enterprise.objects.filter(id=enterprise.id).update(points=enterprise.points + instance.activity.global_points)

            # Guardar la instancia si se ha modificado
            instance.save()
        finally:
            # Volver a conectar la señal
            post_save.connect(update_user, sender=RegisterActivity)

