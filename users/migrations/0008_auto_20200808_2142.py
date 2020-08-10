# Generated by Django 3.0.7 on 2020-08-08 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200805_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachaccount',
            name='IBAN',
            field=models.CharField(default='inconnu', max_length=50, verbose_name='numéro de compte IBAN'),
        ),
        migrations.AlterField(
            model_name='coachaccount',
            name='nationalRegisterID',
            field=models.CharField(default='Inconnu', max_length=50, verbose_name='numéro de registre national'),
        ),
    ]
