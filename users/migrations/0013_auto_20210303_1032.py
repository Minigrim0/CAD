# Generated by Django 3.0.7 on 2021-03-03 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20210303_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='read',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='coachrequestthrough',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.StudentRequest'),
        ),
        migrations.AlterField(
            model_name='studentrequest',
            name='coaches',
            field=models.ManyToManyField(blank=True, related_name='request_participated', through='users.CoachRequestThrough', to='users.CoachAccount'),
        ),
    ]
