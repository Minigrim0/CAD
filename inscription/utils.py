import hashlib

from django.contrib.auth.models import User

from users.models import (CoachAccount, FollowElement, Notification, Profile,
                          StudentAccount)


def sendNotifToCoaches(student):
    # Receive Profile type object
    coaches = Profile.objects.filter(account_type="Coach")
    for coach in coaches:
        if coach.coachaccount.confirmedAccount != "Engage":
            continue
        bMaths = coach.Maths_course == student.Maths_course
        bChimie = coach.Chimie_course == student.Chimie_course
        bPhysique = coach.Physique_course == student.Physique_course
        bFrancais = coach.Francais_course == student.Francais_course
        compatible = bMaths or bChimie or bPhysique or bFrancais
        if coach.school_level == "high":
            same_study_lev = ("eme" in student.school_level)
            same_study_lev = same_study_lev or ("ere" in student.school_level)
            compatible = compatible and same_study_lev
        elif coach.school_level == "elem":
            compatible = compatible and (student.school_level == "primaire")

        if compatible:
            newNotif = Notification(user=coach.user)
            newNotif.author = "{} {}".format(
                student.user.first_name, student.user.last_name)
            newNotif.title = "Recherche de coach"
            newNotif.content = "Vos matières/niveaux correspondent avec "
            newNotif.content += "{} {} ".format(
                student.user.first_name, student.user.last_name)
            newNotif.content += "!\nVous pouvez cliquer "
            newNotif.content += "<a href='/users/requests/{}/'>ici</a>".format(
                student.user.studentrequest.id)
            newNotif.content += " pour voir le profil de l'etudiant"
            newNotif.save()
            coach.save()


def create_notif(user, title, content, author):
    newNotif = Notification(user=user)
    newNotif.title = title
    newNotif.content = content
    newNotif.author = author
    newNotif.save()


def getSchedule(student_profile, form):
    days_array = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday']

    for day in days_array:
        id = "course " + day
        try:
            if form[id] == 'on':
                student_profile.wanted_schedule += "1/"
                student_profile.wanted_schedule += form[day + "Start"] + "/"
                student_profile.wanted_schedule += form[day + "End"] + "."
        except Exception:
            student_profile.wanted_schedule += "0/0/0."
    student_profile.save()


def studentRegister(user, form):
    student_profile = StudentAccount(profile=user.profile)

    student_profile.tutor_name = form.cleaned_data["tutor_name"]
    student_profile.tutor_firstName = form.cleaned_data["tutor_firstName"]
    student_profile.NeedsVisit = form.cleaned_data["NeedsVisit"]
    student_profile.comments = form.cleaned_data["comments"]
    student_profile.zip = form.cleaned_data["zip"]
    student_profile.ville = form.cleaned_data["ville"]
    student_profile.wanted_schedule = form.cleaned_data["wanted_schedule"]
    student_profile.save()

    # Follow Element creation
    folElem = FollowElement(student=user)
    folElem.coach = "L'Equipe CAD"
    folElem.comments = "Inscription sur le site CAD - cours à domicile"
    folElem.save()


def coachRegister(user, form):
    coach_profile = CoachAccount(profile=user.profile)
    coach_profile.school = form.cleaned_data["school"]
    coach_profile.French_level = form.cleaned_data["french_level"]
    coach_profile.English_level = form.cleaned_data["english_level"]
    coach_profile.Dutch_level = form.cleaned_data["dutch_level"]
    coach_profile.IBAN = form.cleaned_data["IBAN"]
    coach_profile.nationalRegisterID = form.cleaned_data["nationalRegisterID"]

    coach_profile.save()


def registerUser(form):
    """Generates a user from a form values

    Args:
        form (Form): [A form (either StudentForm or Coach form, both inheriting from BaseRegisterForm)]

    Returns:
        user: the user newly created
    """

    username = '{}_{}'.format(
        form.cleaned_data['last_name'],
        form.cleaned_data['first_name']
    )
    user = User.objects.create(
        username=username,
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name'],
        email=form.cleaned_data['email'])
    user.set_password(form.cleaned_data['password'])
    user.save()
    return user


def registerProfile(user, form, account_type="Etudiant"):
    profile = Profile(user=user)
    profile.phone_number = form.cleaned_data["phone_number"]
    profile.account_type = account_type
    profile.address = form.cleaned_data["address"]
    profile.birthDate = form.cleaned_data["birthdate"]

    profile.Maths_course = "a" in form.cleaned_data['courses']
    profile.Physique_course = "b" in form.cleaned_data['courses']
    profile.Francais_course = "c" in form.cleaned_data['courses']
    profile.Chimie_course = "d" in form.cleaned_data['courses']

    profile.secret_key = hashlib.sha256(user.username.encode("utf-8")).hexdigest()
    profile.verifiedAccount = False
    profile.school_level = form.cleaned_data["school_level"]

    profile.save()


def getUser(token):
    profile = Profile.objects.filter(secret_key=token)
    if profile.count() == 1:
        return profile.first().user
    return None
