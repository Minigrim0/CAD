import hashlib

from django.contrib.auth.models import User
from django.forms import Form
from django.shortcuts import reverse

import cad.settings as settings
from users.models import CoachAccount, Profile, StudentAccount, Notification
from default.models import Mail


def registerProfile(user: User, form: Form, account_type: str = "Etudiant"):
    """Registers information about a profile

    Args:
        user (User): The user the profile belongs to
        form (Form): The form containing the data to fill the profile with
        account_type (str, optional): The type of account the profile will be for. Defaults to "Etudiant".
    """
    profile = Profile(user=user)
    profile.phone_number = form.cleaned_data["phone_number"]
    profile.account_type = account_type
    profile.address = form.cleaned_data["address"]
    profile.birthDate = form.cleaned_data["birthdate"]

    profile.Maths_course = "a" in form.cleaned_data["courses"]
    profile.Physique_course = "b" in form.cleaned_data["courses"]
    profile.Francais_course = "c" in form.cleaned_data["courses"]
    profile.Chimie_course = "d" in form.cleaned_data["courses"]

    profile.secret_key = hashlib.sha256(user.username.encode("utf-8")).hexdigest()
    profile.verifiedAccount = False
    profile.school_level = form.cleaned_data["school_level"]

    profile.save()


def studentRegister(user: User, form: Form):
    """Registers a student account

    Args:
        user (User): The user the student account belongs to
        form (Form): The form containing the data
    """
    student_profile = StudentAccount(profile=user.profile)

    student_profile.tutor_name = form.cleaned_data["tutor_name"]
    student_profile.tutor_firstName = form.cleaned_data["tutor_firstName"]
    student_profile.NeedsVisit = form.cleaned_data["NeedsVisit"]
    student_profile.comments = form.cleaned_data["comments"]
    student_profile.zip = form.cleaned_data["zip"]
    student_profile.ville = form.cleaned_data["ville"]
    student_profile.wanted_schedule = form.cleaned_data["wanted_schedule"]
    student_profile.resp_phone_number1 = form.cleaned_data["resp_phone_number1"]
    student_profile.resp_phone_number2 = form.cleaned_data["resp_phone_number2"]
    student_profile.resp_phone_number3 = form.cleaned_data["resp_phone_number3"]
    student_profile.save()


def coachRegister(user: User, form: Form):
    """Registers a coach accounr

    Args:
        user (User): The user the coach account belongs to
        form (Form): The form containing the data
    """
    coach_profile = CoachAccount(profile=user.profile)
    coach_profile.school = form.cleaned_data["school"]
    coach_profile.French_level = form.cleaned_data["french_level"]
    coach_profile.English_level = form.cleaned_data["english_level"]
    coach_profile.Dutch_level = form.cleaned_data["dutch_level"]
    coach_profile.IBAN = form.cleaned_data["IBAN"]
    coach_profile.nationalRegisterID = form.cleaned_data["nationalRegisterID"]

    coach_profile.save()


def registerUser(form: Form, usertype: str):
    """Generates a user from a form values

    Args:
        form (Form): A form (either StudentForm or Coach form, both inheriting from BaseRegisterForm)
        usertype (str): The type of account the user has
    Returns:
        user: the user newly created
    """
    username = "{}_{}".format(
        form.cleaned_data["last_name"], form.cleaned_data["first_name"]
    )
    user = User.objects.create(username=username)
    user.first_name = form.cleaned_data["first_name"]
    user.last_name = form.cleaned_data["last_name"]
    user.email = form.cleaned_data["email"]
    user.set_password(form.cleaned_data["password"])
    user.save()

    registerProfile(user, form, usertype)
    if usertype == "a":
        studentRegister(user, form)
    elif usertype == "b":
        coachRegister(user, form)

    return user


def getUser(token: str) -> User:
    """Finds the user corresponding to the secret_key and returns it

    Args:
        token (str): The token from which to retreive the user

    Returns:
        User: A user. Defaults to None
    """
    profile = Profile.objects.filter(secret_key=token)
    if profile.count() == 1:
        return profile.first().user
    return None


def welcomeUser(user: User):
    """Welcomes the new user, by sending him an email and a notification

    Args:
        user (User): The new user
    """
    author = "L'équipe CAD"
    title = "Bienvenue parmi nous!"
    content = "Au nom de toute l'équipe de CAD, \
        nous vous souhaitons la bienvenue! \
        N'oubliez pas que vous pouvez nous contacter \
        si vous avez le moindre souci via ce \
        <a href='{}{}'>formulaire</a>!".format(settings.SITE_DOMAIN, reverse("contact_view"))

    newNotif = Notification(user=user)
    newNotif.title = title
    newNotif.content = content
    newNotif.author = author
    newNotif.save()
    send_confirmation_mail(user)


def send_confirmation_mail(user: User):
    """Sends the confirmation email to the user

    Args:
        user (User): The user to send the email to
    """
    mail = Mail.objects.get(role="a")
    mail.send(user)
