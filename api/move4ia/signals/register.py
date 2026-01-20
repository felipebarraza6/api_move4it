"""Process Registers."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from api.move4ia.models import RegisterActivity, Group, Enterprise
from api.users.models import User


@receiver(post_save, sender=RegisterActivity)
def update_user(sender, instance, created, **kwargs):
    if not created:
        # Desconectar temporalmente la señal para evitar recursión
        post_save.disconnect(update_user, sender=RegisterActivity)

        try:
            if instance.is_completed:

                User.objects.filter(id=instance.user.id).update(
                    points=instance.user.points + instance.activity.points)

            # Guardar la instancia si se ha modificado
            instance.save()
        finally:
            # Volver a conectar la señal
            post_save.connect(update_user, sender=RegisterActivity)
