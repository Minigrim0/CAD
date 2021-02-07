# Generated by Django 3.0.7 on 2021-02-07 12:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0009_auto_20210122_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='FollowElement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.FollowElement'),
        ),
        migrations.AlterField(
            model_name='followelement',
            name='coach',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='coach_of', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='followelement',
            name='student',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
