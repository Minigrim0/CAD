# Generated by Django 3.0.7 on 2020-08-14 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('default', '0004_mailinglist'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Envoyé à'),
        ),
        migrations.AlterField(
            model_name='mail',
            name='role',
            field=models.CharField(choices=[('a', "verification de l'adresse mail"), ('b', 'mail de bienvenue'), ('c', 'proposition desinscription'), ('d', 'solde dangereux'), ('e', 'proposition de mission'), ('f', 'attribution de mission'), ('g', 'mission attribuée à un autre coach'), ('h', 'Template non automatique'), ('i', 'Message envoyé')], max_length=1, verbose_name='Role du mail'),
        ),
    ]
