# Generated by Django 3.0.7 on 2021-03-03 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20210303_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachrequestthrough',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.StudentRequest'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentrequest',
            name='coaches',
            field=models.ManyToManyField(blank=True, related_name='request_participated', through='users.CoachRequestThrough', to='users.CoachAccount'),
        ),
    ]