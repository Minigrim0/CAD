# Generated by Django 3.0.5 on 2020-04-26 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='Article', verbose_name="Nom de l'article")),
                ('title', models.TextField(null=True)),
                ('subTitle', models.TextField(null=True)),
                ('content', models.TextField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date de modification')),
            ],
        ),
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Mail template', max_length=150, verbose_name='Nom de la template')),
                ('subject', models.CharField(default='CAD - Cours à domicile', max_length=150, verbose_name='Sujet')),
                ('content', models.TextField(default='None', verbose_name='Contenu')),
                ('role', models.CharField(choices=[('a', "verification de l'adresse mail"), ('b', 'mail de bienvenue'), ('c', 'proposition desinscription'), ('d', 'solde dangereux'), ('e', 'proposition de mission'), ('f', 'attribution de mission'), ('g', 'mission attribuée à un autre coach'), ('h', 'Template non automatique')], max_length=1, verbose_name='Role du mail')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.TextField(default='No subject')),
                ('content', models.TextField()),
                ('contact_mail', models.CharField(max_length=250)),
            ],
        ),
    ]