from django import utils
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
        Modèle Profile:
            => Extension du modèle User, est utilisé pour sauvegarder les infos
            autant des profils étudiants que des profils coach
    """
    levels = [
        ("a", "Primaire"),
        ("b", "1ère humanité"),
        ("c", "2ème humanité"),
        ("d", "3ème humanité"),
        ("e", "4ème humanité"),
        ("f", "5ème humanité"),
        ("g", "6ème humanité"),
        ("h", "Primaire"),
        ("i", "Humanité"),
        ("j", "Les deux"),
        ("k", "autre")
    ]

    account_types = [
        ("a", "Etudiant"),
        ("b", "Coach"),
        ("c", "Administrateur")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(
        null=True, blank=True, verbose_name="numéro de téléphone",
        default="", max_length=25)
    account_type = models.CharField(
        null=True, blank=True, choices=account_types, default="a", max_length=1,
        verbose_name="Role")
    address = models.CharField(
        null=True, blank=True, default="unknown", max_length=150,
        verbose_name="Adresse de l'étudiant")
    birthDate = models.CharField(
        max_length=25, default="01/01/00", verbose_name="Date de naissance")
    Maths_course = models.BooleanField(
        default=False, verbose_name="Maths")
    Chimie_course = models.BooleanField(
        default=False, verbose_name="Chimie")
    Physique_course = models.BooleanField(
        default=False, verbose_name="Physique")
    Francais_course = models.BooleanField(
        default=False, verbose_name="Francais")
    secret_key = models.CharField(
        null=True, blank=True, default="", max_length=64,
        verbose_name="Clé unique pour l'utilisateur")
    # User has verified his account via mail
    verifiedAccount = models.BooleanField(
        default=False, verbose_name="A vérifié son addresse mail")
    # Represents school level for student
    # Represents either if coach give course to humanité or primaire
    school_level = models.CharField(
        null=True, blank=True, choices=levels, max_length=1,
        verbose_name="Niveau scolaire")

    @property
    def courses(self):
        msg = ""
        if self.Maths_course:
            msg += "Maths, "
        if self.Chimie_course:
            msg += "Chimie, "
        if self.Physique_course:
            msg += "Physique, "
        if self.Francais_course:
            msg += "Francais "
        return msg

    def __repr__(self):
        string = "Nom: {} ".format(self.user.first_name)
        string += "{}\n".format(self.user.last_name)
        string += "Role: {}\n".format(self.account_type)
        if self.account_type == "b":  # If coach
            string += "Donne cours en " + self.school_level + "\n"
        else:
            string += "Est en " + self.school_level + "\n"
        return string

    def __str__(self):
        return "{} {}'s profile".format(
            self.user.first_name, self.user.last_name)


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
    wanted_schedule = models.TextField(
        null=True, blank=True, default="",
        verbose_name="Horaire")
    unsub_proposal = models.BooleanField(
        default=False, verbose_name="Proposition de désinscription envoyée")
    # User has payed the two first hours of course
    coach = models.ForeignKey(
        User, null=True, related_name="Coach", on_delete=models.CASCADE)
    confirmedAccount = models.BooleanField(
        default=False, verbose_name="A payé ses 2 premières heures de cours")
    zip = models.CharField(
        default='0000', max_length=4, blank=True)
    ville = models.CharField(
        max_length=50, default="None", blank=True)

    @property
    def balance(self):
        transactions = Transaction.objects.filter(student=self)
        balance = sum(transaction.amount for transaction in transactions)
        return int(balance)

    def __str__(self):
        return "{} {}'s student profile".format(
            self.profile.user.first_name, self.profile.user.last_name)


class CoachAccount(models.Model):
    coach_states = [
        ('a', '----'),
        ('b', 'Engagé'),
        ('c', 'Refusé'),
    ]

    # Coach
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    school = models.CharField(
        null=True, blank=True, default="None", max_length=50,
        verbose_name="Ecole")
    French_level = models.CharField(
        null=True, blank=True, default="Inconnu", max_length=50)
    English_level = models.CharField(
        null=True, blank=True, default="Inconnu", max_length=50)
    Dutch_level = models.CharField(
        null=True, blank=True, default="Inconnu", max_length=50)
    IBAN = models.CharField(
        null=False, verbose_name="numéro de compte IBAN",
        default="inconnu", max_length=50)
    nationalRegisterID = models.CharField(
        null=False, verbose_name="numéro de registre national",
        default="Inconnu", max_length=50)
    nbStudents = models.IntegerField(
        null=True, blank=True, verbose_name="nombre d'étudiants du coach",
        default=0)
    confirmedAccount = models.CharField(
        default="a", blank=True, choices=coach_states, verbose_name="Etat", max_length=1)


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Name of the author of the notification
    author = models.CharField(
        blank=True, null=True, max_length=50,
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
    student = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, default=DEFAULT_ID)
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


class Transaction(models.Model):
    """
        Modèle transaction:
            => Représente un ajout d'argent par un administrateur sur le compte
            d'un étudiant ou la dépense d'un étudiant pour payment d'un cours
    """

    student = models.ForeignKey(StudentAccount, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=False, default=0)
    date = models.DateTimeField(auto_now_add=True, null=True)
    admin = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300, blank=True)
