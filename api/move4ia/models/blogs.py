from django.db import models
from api.utils.models import ModelApi


class Blog(ModelApi):
    title = models.CharField(max_length=1200, verbose_name='titulo')
    principal_img = models.ImageField(
        blank=True, null=True, upload_to='blog/principal_images/', verbose_name='imagen principal')
    description1 = models.TextField(
        max_length=1200, blank=True, null=True, verbose_name='parrafo 1/titulo foto')
    description2 = models.TextField(
        max_length=1200, blank=True, null=True, verbose_name='parrafo 2')
    description3 = models.TextField(
        max_length=1200, blank=True, null=True, verbose_name='parrafo 3')
    description4 = models.TextField(
        max_length=1200, blank=True, null=True, verbose_name='parrafo 4')
    description5 = models.TextField(
        max_length=1200, blank=True, null=True, verbose_name='parrafo 5')
    types = (
        ('novedades', 'novedades'),
        ('beneficios', 'beneficios'),

    )
    type = models.CharField(max_length=1200, blank=True,
                            null=True, choices=types, verbose_name='tipo')

    def __str__(self):
        # Fix: Return a string representation of the object.
        return str(self.title)
