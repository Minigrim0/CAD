from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from inscription.utils import sendNotifToCoaches
from users.models import studentRequest


def modifyUser(username, form):
    user = get_object_or_404(User, username=username)
    cleaned_data = form.cleaned_data
    user.first_name = cleaned_data['first_name']
    user.last_name = cleaned_data['last_name']
    user.email = cleaned_data['email']
    user.save()

    profile = user.profile
    profile.phone_number = cleaned_data['phone_number']
    profile.address = cleaned_data['address']
    profile.birthDate = cleaned_data['birthdate']
    profile.verifiedAccount = cleaned_data['verifiedAccount']

    if profile.account_type in ['student', 'coach']:
        profile.school_level = cleaned_data['school_level']
        profile.Maths_course = "a" in cleaned_data['courses']
        profile.Physique_course = "b" in cleaned_data['courses']
        profile.Francais_course = "c" in cleaned_data['courses']
        profile.Chimie_course = "d" in cleaned_data['courses']
        if profile.account_type == "student":
            modifyStudent(profile.studentaccount, cleaned_data)
        else:
            modifyCoach(profile.coachaccount, cleaned_data)
    profile.save()


def modifyStudent(student_account, cleaned_data):
    """
        Modifies a student profile according to the given form
    """
    student_account.NeedsVisit = cleaned_data['NeedsVisit']
    student_account.comments = cleaned_data["comments"]
    student_account.tutor_firstName = cleaned_data["tutor_firstName"]
    student_account.tutor_name = cleaned_data["tutor_name"]
    student_account.wanted_schedule = cleaned_data['wanted_schedule']
    student_account.zip = cleaned_data['zip']
    student_account.ville = cleaned_data['ville']
    student_account.zip = cleaned_data['zip']
    student_account.coach = cleaned_data['coach']

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
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'birthdate': user.profile.birthDate,
        'email': user.email,
        'address': user.profile.address,
        'phone_number': user.profile.phone_number,
        'secret_key': user.profile.secret_key,
        'verifiedAccount': user.profile.verifiedAccount,
    }

    if usertype == "student":
        data.update({
            'school_level': user.profile.school_level,
            'tutor_name': user.profile.studentaccount.tutor_name,
            'tutor_firstName': user.profile.studentaccount.tutor_firstName,
            'comments': user.profile.studentaccount.comments,
            'wanted_schedule': user.profile.studentaccount.wanted_schedule,
            'zip': user.profile.studentaccount.zip,
            'ville': user.profile.studentaccount.ville,
            'NeedsVisit': user.profile.studentaccount.NeedsVisit,
            'balance': user.profile.studentaccount.balance,
            'courses': list(filter((None).__ne__, [
                'a' if user.profile.Maths_course else None,
                'b' if user.profile.Physique_course else None,
                'c' if user.profile.Francais_course else None,
                'd' if user.profile.Chimie_course else None,
            ]))
        })
    elif usertype == "coach":
        data.update({
            'school_level': user.profile.school_level,
            'school': user.profile.coachaccount.school,
            'IBAN': user.profile.coachaccount.IBAN,
            'french_level': user.profile.coachaccount.French_level,
            'dutch_level': user.profile.coachaccount.Dutch_level,
            'english_level': user.profile.coachaccount.English_level,
            'nationalRegisterID': user.profile.coachaccount.nationalRegisterID,
            'confirmedAccount': user.profile.coachaccount.confirmedAccount,
            'courses': list(filter((None).__ne__, [
                'a' if user.profile.Maths_course else None,
                'b' if user.profile.Physique_course else None,
                'c' if user.profile.Francais_course else None,
                'd' if user.profile.Chimie_course else None,
            ]))
        })

    return data
