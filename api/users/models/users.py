"""User Model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utils
from api.utils.models import ModelApi
from api.move4it.models import Group
import re
import json


class User(ModelApi, AbstractUser):

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'El usuario ya existe.'
        }
    )

    identification_number = models.CharField(
        max_length=80, verbose_name='(rut o pasaporte)', unique=True)
    gengers = [('M', 'Masculino'), ('F', 'Femenino')]
    gender = models.CharField(
        max_length=30, verbose_name='Género', blank=True, null=True, choices=gengers)
    phone_number = models.CharField(
        verbose_name='Telefono', max_length=500, blank=True, null=True)

    PROFILES = [
        ('ADM', 'administrator'),
        ('ADC', 'admin_client'),
        ('CF', 'client'),
    ]

    type_user = models.CharField(
        max_length=3, verbose_name='Tipo de usuario', choices=PROFILES)

    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'identification_number', 'type_user',]
    points = models.IntegerField(default=0, verbose_name='puntos')

    is_verified = models.BooleanField(
        verbose_name='verificado',
        default=True,
        help_text='Se establece en verdadero cuando el usuario ha verificado su dirección de correo electrónico'
    )

    is_leader = models.BooleanField(
        verbose_name='es lider',
        default=False,
        help_text='Se establece en verdadero cuando el usuario es lider de su grupo'
    )

    username = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        unique=True,
        help_text='Deje este campo en blanco para generar automáticamente un nombre de usuario.'
    )

    USERNAME_FIELD = 'email'
    group_participation = models.ForeignKey(
        Group, on_delete=models.CASCADE, verbose_name='Equipo de participación', null=True, blank=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def save(self, *args, **kwargs):
        # Check if this is a new user
        if len(self.identification_number) == 9:
            self.identification_number = f"{self.identification_number[:2]}.{self.identification_number[2:5]}.{
                self.identification_number[5:8]}-{self.identification_number[8]}"
        elif len(self.identification_number) == 10:
            self.identification_number = f"{self.identification_number[:2]}.{self.identification_number[2:5]}.{
                self.identification_number[5:8]}-{self.identification_number[8:]}"

        super().save(*args, **kwargs)
