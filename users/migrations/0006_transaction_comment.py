# Generated by Django 3.0.7 on 2020-08-04 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_studentaccount_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='comment',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
