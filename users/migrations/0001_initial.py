# Generated by Django 3.0.7 on 2020-09-12 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CoachAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(blank=True, default='None', max_length=50, null=True, verbose_name='Ecole')),
                ('French_level', models.CharField(blank=True, default='Inconnu', max_length=50, null=True)),
                ('English_level', models.CharField(blank=True, default='Inconnu', max_length=50, null=True)),
                ('Dutch_level', models.CharField(blank=True, default='Inconnu', max_length=50, null=True)),
                ('IBAN', models.CharField(default='inconnu', max_length=50, verbose_name='numéro de compte IBAN')),
                ('nationalRegisterID', models.CharField(default='Inconnu', max_length=50, verbose_name='numéro de registre national')),
                ('confirmedAccount', models.CharField(blank=True, choices=[('a', '----'), ('b', 'Engagé'), ('c', 'Refusé')], default='a', max_length=1, verbose_name='Etat')),
            ],
        ),
        migrations.CreateModel(
            name='coachRequestThrough',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coachschedule', models.TextField()),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CoachAccount')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, default='', max_length=25, null=True, verbose_name='numéro de téléphone')),
                ('account_type', models.CharField(blank=True, choices=[('a', 'Etudiant'), ('b', 'Coach'), ('c', 'Administrateur')], default='a', max_length=1, null=True, verbose_name='Role')),
                ('address', models.CharField(blank=True, default='unknown', max_length=150, null=True, verbose_name="Adresse de l'étudiant")),
                ('birthDate', models.CharField(default='01/01/00', max_length=25, verbose_name='Date de naissance')),
                ('Maths_course', models.BooleanField(default=False, verbose_name='Maths')),
                ('Chimie_course', models.BooleanField(default=False, verbose_name='Chimie')),
                ('Physique_course', models.BooleanField(default=False, verbose_name='Physique')),
                ('Francais_course', models.BooleanField(default=False, verbose_name='Francais')),
                ('secret_key', models.CharField(blank=True, default='', max_length=64, null=True, verbose_name="Clé unique pour l'utilisateur")),
                ('verifiedAccount', models.BooleanField(default=False, verbose_name='A vérifié son addresse mail')),
                ('school_level', models.CharField(blank=True, choices=[('a', 'Primaire'), ('b', '1ère humanité'), ('c', '2ème humanité'), ('d', '3ème humanité'), ('e', '4ème humanité'), ('f', '5ème humanité'), ('g', '6ème humanité'), ('h', 'Primaire'), ('i', 'Humanité'), ('j', 'Les deux'), ('k', 'autre')], max_length=1, null=True, verbose_name='Niveau scolaire')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tutor_name', models.CharField(blank=True, default='inconnu', max_length=50, null=True, verbose_name='Nom du tuteur')),
                ('tutor_firstName', models.CharField(blank=True, default='inconnu', max_length=50, null=True, verbose_name='Prénom du tuteur')),
                ('NeedsVisit', models.BooleanField(default=False, verbose_name='Désire une visite pédagogique ?')),
                ('comments', models.TextField(blank=True, default='Aucun commentaire', null=True, verbose_name='Commentaires')),
                ('wanted_schedule', models.TextField(blank=True, default='', null=True, verbose_name='Horaire')),
                ('unsub_proposal', models.BooleanField(default=False, verbose_name='Proposition de désinscription envoyée')),
                ('confirmedAccount', models.BooleanField(default=False, verbose_name='A payé ses 2 premières heures de cours')),
                ('zip', models.CharField(blank=True, default='0000', max_length=4)),
                ('ville', models.CharField(blank=True, default='None', max_length=50)),
                ('resp_phone_number1', models.CharField(blank=True, default='', max_length=25, null=True, verbose_name="numéro de téléphone d'un responsable")),
                ('resp_phone_number2', models.CharField(blank=True, default='', max_length=25, null=True, verbose_name="numéro de téléphone d'un responsable")),
                ('resp_phone_number3', models.CharField(blank=True, default='', max_length=25, null=True, verbose_name="numéro de téléphone d'un responsable")),
                ('coach', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='users.CoachAccount')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('comment', models.CharField(blank=True, max_length=300)),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.StudentAccount')),
            ],
        ),
        migrations.CreateModel(
            name='studentRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_closed', models.BooleanField(default=False)),
                ('choosenCoach', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.CoachAccount')),
                ('coaches', models.ManyToManyField(blank=True, related_name='request_participated', through='users.coachRequestThrough', to='users.CoachAccount')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(blank=True, max_length=50, null=True, verbose_name='Auteur de la notification')),
                ('title', models.CharField(blank=True, max_length=50, null=True, verbose_name='Titre de la notification')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Contenu de la notification')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FollowElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coach', models.CharField(blank=True, default='Erreur lors de la recherche du coach', max_length=110, null=True)),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Date et heure du cours')),
                ('comments', models.TextField(blank=True, default='Pas de commentaires', null=True, verbose_name='Commentaires du cours')),
                ('student', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='coachrequestthrough',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.studentRequest'),
        ),
        migrations.AddField(
            model_name='coachaccount',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.Profile'),
        ),
    ]
