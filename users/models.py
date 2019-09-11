from django.db import models
from django.contrib.auth.models import User
from django import utils


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Both accounts type
    phone_number = models.IntegerField(
        null=True, blank=True, verbose_name="numéro de téléphone", default=0)
    account_type = models.CharField(
        null=True, blank=True, default="unknown", max_length=50,
        verbose_name="Role")
    address = models.CharField(
        null=True, blank=True, default="unknown", max_length=150,
        verbose_name="Adresse de l'étudiant")
    birthDate = models.DateField(
        auto_now=False, auto_now_add=False, default="2019-01-01",
        verbose_name="Date de naissance")

    notifications_nb = models.IntegerField(
        null=True, blank=True, default=0,
        verbose_name="Nombre de notifications")

    Maths_course = models.BooleanField(
        default=False, verbose_name="Maths")
    Chimie_course = models.BooleanField(
        default=False, verbose_name="Chimie")
    Physique_course = models.BooleanField(
        default=False, verbose_name="Physique")
    Francais_course = models.BooleanField(
        default=False, verbose_name="Francais")

    secret_key = models.CharField(
        null=True, blank=True, default="", max_length=20,
        verbose_name="Clé unique pour l'utilisateur")
    verifiedAccount = models.BooleanField(
        default=False, verbose_name="A vérifié son addresse mail")

    # Current level for student - Course level for coach
    school_level = models.CharField(
        null=True, blank=True, default="None", max_length=50,
        verbose_name="Souhaite donner cours en")

    # Student
    tutor_name = models.CharField(
        null=True, blank=True, default="inconnu", max_length=50,
        verbose_name="Nom du tuteur")
    tutor_firstName = models.CharField(
        null=True, blank=True, default="inconnu", max_length=50,
        verbose_name="Prénom du tuteur")

    NeedsVisit = models.BooleanField(
        default=False, verbose_name="Désire une visite pédagogique ?")
    comments = models.TextField(
        null=True, blank=True, verbose_name="Commentaires",
        default="Aucun commentaire")

    # . -> sépare les jours, / sépare les valeurs
    # => 0/0/0 = Pas de cours ce jour là
    wanted_schedule = models.CharField(
        null=True, blank=True, default="",
        verbose_name="Horaire", max_length=42)

    balance = models.IntegerField(
        null=True, blank=True, verbose_name="Solde", default=0)
    confirmed_account = models.BooleanField(
        default=False, verbose_name="A payé ses 2 premières heures de cours")

    # Coach
    school = models.CharField(
        null=True, blank=True, default="None",  max_length=50,
        verbose_name="Ecole")

    French_level = models.CharField(
        null=True, blank=True, default="Inconnu", max_length=50)
    English_level = models.CharField(
        null=True, blank=True, default="Inconnu", max_length=50)
    Dutch_level = models.CharField(
        null=True, blank=True, default="Inconnu", max_length=50)

    IBAN = models.CharField(
        null=True, blank=True, verbose_name="numéro de compte IBAN",
        default="inconnu", max_length=50)
    nationalRegisterID = models.CharField(
        null=True, blank=True, verbose_name="numéro de registre national",
        default="Inconnu", max_length=50)

    nbStudents = models.IntegerField(
        null=True, blank=True, verbose_name="nombre d'étudiants qu'à ce coach",
        default=0)

    def setAccountType(self, type):
        if type == "student":
            self.account_type = "Etudiant"
        elif type == "coach":
            self.account_type = "Coach"

    def __repr__(self):
        string = "Nom : {} ".format(self.user.first_name)
        string += "{}\n".format(self.user.last_name)
        string += "Role : {}\n".format(self.account_type)
        if self.account_type == "Coach":
            string += "Donne cours en " + self.school_level + "\n"
        else:
            string += "Est en " + self.school_level + "\n"
        return string


class studentRequest(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    coaches = models.ManyToManyField(Profile)


class Notification(models.Model):
    user = models.ForeignKey(User)

    author = models.CharField(
        blank=True, null=True,  max_length=50,
        verbose_name="Auteur de la notification")
    title = models.CharField(
        blank=True, null=True, max_length=50,
        verbose_name="Titre de la notification")
    content = models.TextField(
        blank=True, null=True, verbose_name="Contenu de la notification")


DEFAULT_ID = 1


class FollowElement(models.Model):
    student = models.ForeignKey(User, blank=True, default=DEFAULT_ID)
    coach = models.CharField(
        null=True, blank=True, max_length=110,
        default="Erreur lors de la recherche du coach")

    date = models.DateTimeField(
        default=utils.timezone.now, blank=True,
        verbose_name="Date et heure du cours")
    comments = models.TextField(
        null=True, blank=True, default="Pas de commentaires",
        verbose_name="Commentaires du cours")
