# Generated by Django 5.0.8 on 2024-08-06 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('move4it', '0027_remove_registeractivity_user_assigned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registeractivity',
            name='is_finished',
        ),
        migrations.AddField(
            model_name='registeractivity',
            name='is_load',
            field=models.BooleanField(default=False, verbose_name='cargo evidencia'),
        ),
    ]
