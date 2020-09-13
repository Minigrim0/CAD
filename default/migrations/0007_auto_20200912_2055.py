# Generated by Django 3.0.7 on 2020-09-12 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0006_auto_20200912_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='role',
            field=models.CharField(choices=[('a', "verification de l'adresse mail"), ('b', 'mail de bienvenue'), ('c', 'proposition desinscription'), ('d', 'solde dangereux'), ('e', 'proposition de mission'), ('f', 'attribution de mission'), ('g', 'mission attribuée à un autre coach'), ('h', 'Template non automatique'), ('i', 'Message envoyé')], max_length=1, verbose_name='Role du mail'),
        ),
    ]