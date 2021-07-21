from django import utils
from django.contrib.auth.models import User
from django.db import models

from datetime import datetime
from default.models import Mail


class Profile(models.Model):
    """The extension of the user model"""

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
        ("k", "autre"),
    ]
    account_types = [("a", "Etudiant"), ("b", "Coach"), ("c", "Administrateur")]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(
        null=True,
        blank=True,
        verbose_name="numéro de téléphone",
        default="",
        max_length=25,
    )
    account_type = models.CharField(
        null=True,
        blank=True,
        choices=account_types,
        default="a",
        max_length=1,
        verbose_name="Role",
    )
    address = models.CharField(
        null=True,
        blank=True,
        default="unknown",
        max_length=150,
        verbose_name="Adresse de l'étudiant",
    )
    birthDate = models.CharField(max_length=25, default="01/01/00", verbose_name="Date de naissance")
    Maths_course = models.BooleanField(default=False, verbose_name="Maths")
    Chimie_course = models.BooleanField(default=False, verbose_name="Chimie")
    Physique_course = models.BooleanField(default=False, verbose_name="Physique")
    Francais_course = models.BooleanField(default=False, verbose_name="Francais")
    secret_key = models.CharField(
        null=True,
        blank=True,
        default="",
        max_length=64,
        verbose_name="Clé unique pour l'utilisateur",
    )
    verifiedAccount = models.BooleanField(default=False, verbose_name="A vérifié son addresse mail")
    # Represents school level for student
    # Represents either if coach give course to humanité or primaire
    school_level = models.CharField(
        null=True,
        blank=True,
        choices=levels,
        max_length=1,
        verbose_name="Niveau scolaire",
    )

    @property
    def courses(self):
        """Returns a string containing the diffrent courses of this profile

        Returns:
            str: The courses, comma separated
        """
        msg = ""
        if self.Maths_course:
            msg += "Maths, "
        if self.Chimie_course:
            msg += "Chimie, "
        if self.Physique_course:
            msg += "Physique, "
        if self.Francais_course:
            msg += "Francais"
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
        return "{} {}'s profile".format(self.user.first_name, self.user.last_name)


class StudentAccount(models.Model):
    """A student account, depending on a profile"""

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    tutor_name = models.CharField(
        null=True,
        blank=True,
        default="inconnu",
        max_length=50,
        verbose_name="Nom du tuteur",
    )
    tutor_firstName = models.CharField(
        null=True,
        blank=True,
        default="inconnu",
        max_length=50,
        verbose_name="Prénom du tuteur",
    )
    NeedsVisit = models.BooleanField(default=False, verbose_name="Désire une visite pédagogique ?")
    comments = models.TextField(null=True, blank=True, verbose_name="Commentaires", default="Aucun commentaire")
    wanted_schedule = models.TextField(null=True, blank=True, default="", verbose_name="Horaire")
    unsub_proposal = models.BooleanField(default=False, verbose_name="Proposition de désinscription envoyée")
    # User has payed the two first hours of course
    coach = models.ForeignKey(
        "users.CoachAccount",
        null=True,
        blank=True,
        related_name="students",
        on_delete=models.SET_NULL,
    )
    confirmedAccount = models.BooleanField(default=False, verbose_name="A payé ses 2 premières heures de cours")
    zip = models.CharField(default="0000", max_length=4, blank=True)
    ville = models.CharField(max_length=50, default="None", blank=True)
    resp_phone_number1 = models.CharField(
        null=True,
        blank=True,
        verbose_name="numéro de téléphone d'un responsable",
        default="",
        max_length=25,
    )
    resp_phone_number2 = models.CharField(
        null=True,
        blank=True,
        verbose_name="numéro de téléphone d'un responsable",
        default="",
        max_length=25,
    )
    resp_phone_number3 = models.CharField(
        null=True,
        blank=True,
        verbose_name="numéro de téléphone d'un responsable",
        default="",
        max_length=25,
    )

    @property
    def balance(self):
        """Returns the balance of the student account base on previous transactions

        Returns:
            int: The calculated balance
        """
        transactions = Transaction.objects.filter(student=self)
        balance = sum(transaction.amount for transaction in transactions)
        return round(balance, 2)

    def __str__(self):
        return "{} {}'s student profile".format(
            self.profile.user.first_name, self.profile.user.last_name
        )


class CoachAccount(models.Model):
    """A coach account depending on a profile"""

    coach_states = [
        ("a", "----"),
        ("b", "Engagé"),
        ("c", "Refusé"),
    ]

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    school = models.CharField(null=True, blank=True, default="None", max_length=50, verbose_name="Ecole")
    French_level = models.CharField(null=True, blank=True, default="Inconnu", max_length=50)
    English_level = models.CharField(null=True, blank=True, default="Inconnu", max_length=50)
    Dutch_level = models.CharField(null=True, blank=True, default="Inconnu", max_length=50)
    IBAN = models.CharField(
        null=False,
        verbose_name="numéro de compte IBAN",
        default="inconnu",
        max_length=50,
    )
    nationalRegisterID = models.CharField(
        null=False,
        verbose_name="numéro de registre national",
        default="Inconnu",
        max_length=50,
    )
    confirmedAccount = models.CharField(
        default="a", blank=True, choices=coach_states, verbose_name="Etat", max_length=1
    )

    @property
    def nb_students(self):
        """Returns the amount of students the coach has

        Returns:
            int: The amount of students
        """
        return self.students.count()

    def schedule(self, studentRequest):
        """Returns the schedule of the coach for the given Student Request"""
        if studentRequest.coachrequestthrough_set.filter(coach=self).count() == 1:
            return studentRequest.coachrequestthrough_set.get(coach=self).coachschedule
        return ""

    def __str__(self):
        return "{} {}".format(self.profile.user.first_name, self.profile.user.last_name)


class CoachRequestThrough(models.Model):
    """The in between model for the coach account to the request"""

    request = models.ForeignKey("users.StudentRequest", on_delete=models.CASCADE)
    coach = models.ForeignKey("users.CoachAccount", on_delete=models.CASCADE)

    coachschedule = models.TextField(null=False, blank=False)
    has_accepted = models.BooleanField(default=True)


class StudentRequest(models.Model):
    """A request for a coach from a student"""

    # represents the user who made the request
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    # represents the coaches who accepted this request
    coaches = models.ManyToManyField(
        "users.CoachAccount",
        blank=True,
        related_name="request_participated",
        through="users.CoachRequestThrough",
    )
    is_closed = models.BooleanField(default=False)
    choosenCoach = models.ForeignKey(
        "users.CoachAccount", blank=True, null=True, on_delete=models.SET_NULL
    )
    finalschedule = models.TextField(null=True, blank=True)


class Notification(models.Model):
    """Represents a notification sent to a user"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(
        blank=True, null=True, max_length=50, verbose_name="Auteur de la notification"
    )
    title = models.CharField(
        blank=True, null=True, max_length=50, verbose_name="Titre de la notification"
    )
    content = models.TextField(
        blank=True, null=True, verbose_name="Contenu de la notification"
    )
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    read = models.BooleanField(default=False)

    def send_as_mail(self):
        """Sends the notification to the concerned user by email"""
        mail = Mail(
            name="notification - {}".format(self.title),
            subject="Nouvelle notification - {}".format(self.title),
            content=self.content,
            role="i",  # Sent message
            to=self.user,
        )

        mail.send(self.user)


class FollowElement(models.Model):
    """Represents course given by a coach to a student"""

    student = models.ForeignKey(User, blank=True, on_delete=models.PROTECT)
    coach = models.ForeignKey(
        User, blank=True, related_name="coach_of", on_delete=models.PROTECT
    )
    date = models.DateField(
        default=utils.timezone.now, verbose_name="Date et heure du cours"
    )
    startHour = models.TimeField(default="10:00", verbose_name="Heure de début")
    endHour = models.TimeField(default="12:00", verbose_name="Heure de fin")

    # comments of the coach about the course represented by this FollowElement
    comments = models.TextField(
        default="Pas de commentaires", verbose_name="Commentaires du cours"
    )
    approved = models.BooleanField(default=False)

    @property
    def duration(self) -> int:
        """Returns the duration of the course"""
        time = datetime.combine(datetime.today(), self.endHour) - datetime.combine(
            datetime.today(), self.startHour
        )
        return round(time.seconds / 3600, 2)


class Transaction(models.Model):
    """Represents a movement of currency (hours), may be linked to a course"""

    student = models.ForeignKey(StudentAccount, on_delete=models.CASCADE)
    amount = models.FloatField(blank=False, default=0)
    date = models.DateTimeField(auto_now_add=True, null=True)
    admin = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300, blank=True)
    FollowElement = models.ForeignKey(
        "users.followElement", null=True, blank=True, on_delete=models.CASCADE
    )
