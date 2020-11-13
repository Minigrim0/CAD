# Generated by Django 3.0.7 on 2020-11-13 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0005_auto_20201101_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followelement',
            name='coach',
            field=models.CharField(default='Erreur lors de la recherche du coach', max_length=110),
        ),
        migrations.AlterField(
            model_name='followelement',
            name='comments',
            field=models.TextField(default='Pas de commentaires', verbose_name='Commentaires du cours'),
        ),
        migrations.AlterField(
            model_name='followelement',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date et heure du cours'),
        ),
        migrations.AlterField(
            model_name='followelement',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
