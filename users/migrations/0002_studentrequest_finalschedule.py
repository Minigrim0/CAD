# Generated by Django 3.0.7 on 2020-10-15 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentrequest',
            name='finalschedule',
            field=models.TextField(blank=True, null=True),
        ),
    ]
