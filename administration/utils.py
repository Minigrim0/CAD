from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User

from users.models import (
    Profile,
    Notification,
    CoachRequestThrough,
    StudentRequest,
    CoachAccount,
    StudentAccount,
)


def modifyUser(username, form):
    """
    Modifies a user and his profile according to the given form
    """
    user = get_object_or_404(User, username=username)
    cleaned_data = form.cleaned_data
    user.first_name = cleaned_data["first_name"]
    user.last_name = cleaned_data["last_name"]
    user.email = cleaned_data["email"]
    user.save()

    profile = user.profile
    profile.phone_number = cleaned_data["phone_number"]
    profile.address = cleaned_data["address"]
    profile.birthDate = cleaned_data["birthdate"]
    profile.verifiedAccount = cleaned_data["verifiedAccount"]

    if profile.account_type in "ab":
        profile.school_level = cleaned_data["school_level"]
        profile.Maths_course = "a" in cleaned_data["courses"]
        profile.Physique_course = "b" in cleaned_data["courses"]
        profile.Francais_course = "c" in cleaned_data["courses"]
        profile.Chimie_course = "d" in cleaned_data["courses"]
        if profile.account_type == "a":
            modifyStudent(profile.studentaccount, cleaned_data)
        else:
            modifyCoach(profile.coachaccount, cleaned_data)
    profile.save()


def modifyStudent(student_account, cleaned_data):
    """
    Modifies a student profile according to the given form
    """
    student_account.NeedsVisit = cleaned_data["NeedsVisit"]
    student_account.comments = cleaned_data["comments"]
    student_account.tutor_firstName = cleaned_data["tutor_firstName"]
    student_account.tutor_name = cleaned_data["tutor_name"]
    student_account.wanted_schedule = cleaned_data["wanted_schedule"]
    student_account.zip = cleaned_data["zip"]
    student_account.ville = cleaned_data["ville"]
    student_account.zip = cleaned_data["zip"]
    student_account.coach = cleaned_data["coach"]
    student_account.resp_phone_number1 = cleaned_data["resp_phone_number1"]
    student_account.resp_phone_number2 = cleaned_data["resp_phone_number2"]
    student_account.resp_phone_number3 = cleaned_data["resp_phone_number3"]

    student_account.save()


def modifyCoach(coach_account, cleaned_data):
    """
    Modifies a coach profile according to the given form
    """
    coach_account.school = cleaned_data["school"]
    coach_account.IBAN = cleaned_data["IBAN"]
    coach_account.nationalRegisterID = cleaned_data["nationalRegisterID"]
    coach_account.French_level = cleaned_data["french_level"]
    coach_account.English_level = cleaned_data["english_level"]
    coach_account.Dutch_level = cleaned_data["dutch_level"]
    coach_account.confirmedAccount = cleaned_data["confirmedAccount"]

    coach_account.save()


def populate_data(usertype, user):
    """
    Populates a form according to the user's data
    """
    data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "birthdate": user.profile.birthDate,
        "email": user.email,
        "address": user.profile.address,
        "phone_number": user.profile.phone_number,
        "secret_key": user.profile.secret_key,
        "verifiedAccount": user.profile.verifiedAccount,
    }

    if usertype == "a":
        data.update(
            {
                "school_level": user.profile.school_level,
                "tutor_name": user.profile.studentaccount.tutor_name,
                "tutor_firstName": user.profile.studentaccount.tutor_firstName,
                "comments": user.profile.studentaccount.comments,
                "wanted_schedule": user.profile.studentaccount.wanted_schedule,
                "zip": user.profile.studentaccount.zip,
                "ville": user.profile.studentaccount.ville,
                "NeedsVisit": user.profile.studentaccount.NeedsVisit,
                "balance": user.profile.studentaccount.balance,
                "resp_phone_number1": user.profile.studentaccount.resp_phone_number1,
                "resp_phone_number2": user.profile.studentaccount.resp_phone_number2,
                "resp_phone_number3": user.profile.studentaccount.resp_phone_number3,
                "coach": user.profile.studentaccount.coach,
                "courses": list(
                    filter(
                        (None).__ne__,
                        [
                            "a" if user.profile.Maths_course else None,
                            "b" if user.profile.Physique_course else None,
                            "c" if user.profile.Francais_course else None,
                            "d" if user.profile.Chimie_course else None,
                        ],
                    )
                ),
            }
        )
    elif usertype == "b":
        data.update(
            {
                "school_level": user.profile.school_level,
                "school": user.profile.coachaccount.school,
                "IBAN": user.profile.coachaccount.IBAN,
                "french_level": user.profile.coachaccount.French_level,
                "dutch_level": user.profile.coachaccount.Dutch_level,
                "english_level": user.profile.coachaccount.English_level,
                "nationalRegisterID": user.profile.coachaccount.nationalRegisterID,
                "confirmedAccount": user.profile.coachaccount.confirmedAccount,
                "courses": list(
                    filter(
                        (None).__ne__,
                        [
                            "a" if user.profile.Maths_course else None,
                            "b" if user.profile.Physique_course else None,
                            "c" if user.profile.Francais_course else None,
                            "d" if user.profile.Chimie_course else None,
                        ],
                    )
                ),
            }
        )

    return data


def thanksCoaches(coaches, student):
    """
    Sends a notification to the coaches who have not been selected for a specific request
    """

    author = "L'équipe CAD"
    title = "Merci d'avoir répondu présent"
    content = """Merci d'avoir répondu présent à la requête de {} {}.
    Malheureusement, vous n'avez pas été choisi pour donner cours à
    cet étudiant. Mais ne vous en faites pas, votre tour viendra!""".format(
        student.profile.user.first_name, student.profile.user.last_name
    )
    for coach in coaches:
        if (
            CoachRequestThrough.objects.get(
                coach=coach, request__student=student.profile.user
            ).has_accepted
            is True
        ):
            new_notif = Notification(
                user=coach.profile.user, author=author, title=title, content=content
            )
            new_notif.save()
            new_notif.send_as_mail()


def sendNotifToCoaches(student: Profile, request: StudentRequest):
    """
    Looks for coaches compatible with the student request
    """

    # TODO: Upgrade this part
    coaches = Profile.objects.filter(account_type="b")
    for coach in coaches:
        if coach.coachaccount.confirmedAccount != "b":
            continue
        bMaths = coach.Maths_course == student.Maths_course
        bChimie = coach.Chimie_course == student.Chimie_course
        bPhysique = coach.Physique_course == student.Physique_course
        bFrancais = coach.Francais_course == student.Francais_course
        compatible = bMaths or bChimie or bPhysique or bFrancais
        if coach.school_level == "i":
            same_study_lev = student.school_level in "abcdefg"
            compatible = compatible and same_study_lev
        elif coach.school_level == "h":
            compatible = compatible and (student.school_level == "a")

        if compatible:
            newNotif = Notification(user=coach.user)
            newNotif.author = "{} {}".format(
                student.user.first_name, student.user.last_name
            )
            newNotif.title = "Recherche de coach"
            newNotif.content = "Vos matières/niveaux correspondent avec "
            newNotif.content += f"{student.user.first_name} {student.user.last_name} "
            newNotif.content += "!\nVous pouvez cliquer "
            newNotif.content += (
                f"<a href='{reverse('request_view')}?id={request.id}'>ici</a>"
            )
            newNotif.content += " pour voir le profil de l'etudiant"
            newNotif.save()
            newNotif.send_as_mail()
            coach.save()


def create_studentRequest(student: User):
    """Creates a request for the given user, and notifies the appropriate coaches

    Args:
        student (User): The user object to create a request to
    """
    request = StudentRequest.objects.create(student=student)
    sendNotifToCoaches(student.profile, request)
