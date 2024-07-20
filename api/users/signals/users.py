from django.core.mail import EmailMultiAlternatives, send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from api.users.models import Profile, User
from django_rest_passwordreset.signals import reset_password_token_created
from django.db.models.signals import post_save
import re

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(instance.first_name)
        username = f"{instance.first_name.lower()}.{instance.last_name.lower()}.{instance.id}"
        username = re.sub(r'\.', '', username)
        Profile.objects.create(user=instance)
        User.objects.filter(id=instance.id).update(username=username)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    subject = 'RECUPERAR CONTRASEÑA - Move4it'
    from_email = '<contacto@move4it.cl>'
    content = render_to_string(
        'email/user_reset_password.html',
        {
            'current_user': reset_password_token.user,
            'username': reset_password_token.user.username,
            'email': reset_password_token.user.email,
            'reset_password_url': "http://localhost:3000/reset_password/{}/{}".format(
                reset_password_token.key,
                reset_password_token.user.email
                )
        }
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [reset_password_token.user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()
