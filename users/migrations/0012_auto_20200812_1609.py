# Generated by Django 3.0.7 on 2020-08-12 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20200811_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account_type',
            field=models.CharField(blank=True, choices=[('a', 'Etudiant'), ('b', 'Coach'), ('c', 'Administrateur')], default='a', max_length=1, null=True, verbose_name='Role'),
        ),
    ]