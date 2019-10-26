from django.db import models
from django.contrib.auth.models import User
from django import utils


class Profile(models.Model):
    """
        Modèle Profile:
            => Extension du modèle User, est utilisé pour sauvegarder les infos
            autant des profils étudiants que des profils coach
    """

    # Both type of account
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(
        null=True, blank=True, verbose_name="numéro de téléphone",
        default="", max_length=10)
    account_type = models.CharField(
        null=True, blank=True, default="unknown", max_length=50,
        verbose_name="Role")
    address = models.CharField(
        null=True, blank=True, default="unknown", max_length=150,
        verbose_name="Adresse de l'étudiant")
    birthDate = models.DateField(
        auto_now=False, auto_now_add=False, default="2019-01-01",
        verbose_name="Date de naissance")
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
    # User has verified his account via mail
    verifiedAccount = models.BooleanField(
        default=False, verbose_name="A vérifié son addresse mail")
    # Represents school level for student
    # Represents either if coach give course to humanité or primaire
    school_level = models.CharField(
        null=True, blank=True, default="None", max_length=50,
        verbose_name="Niveau scolaire")

    def __repr__(self):
        string = "Nom : {} ".format(self.user.first_name)
        string += "{}\n".format(self.user.last_name)
        string += "Role : {}\n".format(self.account_type)
        if self.account_type == "Coach":
            string += "Donne cours en " + self.school_level + "\n"
        else:
            string += "Est en " + self.school_level + "\n"
        return string


class StudentAccount(models.Model):
    # Student
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

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
    wanted_schedule = models.CharField(
        null=True, blank=True, default="",
        verbose_name="Horaire", max_length=42)
    # Amount left for the student to pay courses
    balance = models.IntegerField(
        null=True, blank=True, verbose_name="Solde", default=0)
    # User as payed the two first hours of course
    confirmed_account = models.BooleanField(
        default=False, verbose_name="A payé ses 2 premières heures de cours")
    coach = models.ForeignKey(
        User, null=True, related_name="Coach", on_delete=models.CASCADE)


class CoachAccount(models.Model):
    # Coach
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

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


class studentRequest(models.Model):
    """
        Modèle studentRequest:
            => Représente une recherche de coach de la part d'un etudiant
    """

    # represents the user who made the request
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    # represents the coaches who accepted this request
    coaches = models.ManyToManyField(Profile)
    is_closed = models.BooleanField(default=False)
    choosenCoach = models.CharField(
        null=True, default='Pas encore de coach choisi', max_length=100)


class Notification(models.Model):
    """
        Modèle Notification:
            => Représente une notification envoyée à un utilisateur
    """

    # represents the user whom the notifiaction is for
    user = models.ForeignKey(User)

    # Name of the author of the notification
    author = models.CharField(
        blank=True, null=True,  max_length=50,
        verbose_name="Auteur de la notification")
    # Title of the notification
    title = models.CharField(
        blank=True, null=True, max_length=50,
        verbose_name="Titre de la notification")
    # body of the notification (Html)
    content = models.TextField(
        blank=True, null=True, verbose_name="Contenu de la notification")
    # Date of the creation
    date_created = models.DateField(
        auto_now_add=True, null=True)


DEFAULT_ID = 1


class FollowElement(models.Model):
    """
        Modèle FollowElement:
            => Représente un élément du suivit de l'élève
    """

    # students whom this followElement is for
    student = models.ForeignKey(User, blank=True, default=DEFAULT_ID)
    # Name of the coach who wrote this followElement
    coach = models.CharField(
        null=True, blank=True, max_length=110,
        default="Erreur lors de la recherche du coach")
    # date of the writing of this FollowElement
    date = models.DateTimeField(
        default=utils.timezone.now, blank=True,
        verbose_name="Date et heure du cours")
    # comments of the coach about the course represented by this FollowElement
    comments = models.TextField(
        null=True, blank=True, default="Pas de commentaires",
        verbose_name="Commentaires du cours")
