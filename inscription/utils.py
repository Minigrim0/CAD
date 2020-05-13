from django.contrib.auth.models import User

from users.models import Profile, Notification, FollowElement, \
    StudentAccount, CoachAccount


def sendNotifToCoaches(student):
    # Receive Profile type object
    coaches = Profile.objects.filter(account_type="Coach")
    for coach in coaches:
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
                student_profile.wanted_schedule += form[day+"Start"] + "/"
                student_profile.wanted_schedule += form[day+"End"] + "."
        except Exception:
            student_profile.wanted_schedule += "0/0/0."
    student_profile.save()


def studentRegister(user, form):
    student_profile = StudentAccount(profile=user.profile)

    student_profile.tutor_name = form["tutorLastName"]
    student_profile.tutor_firstName = form["tutorFirstName"]
    student_profile.NeedsVisit = form["Visit"] != "NoVisit"
    student_profile.comments = form["comments"]
    student_profile.zip = form["zip"]
    student_profile.ville = form["city"]
    student_profile.wanted_schedule = form["schedule"]
    student_profile.save()

    # Follow Element creation
    folElem = FollowElement(student=user)
    folElem.coach = "L'Equipe CAD"
    folElem.comments = "Inscription sur le site CAD - cours à domicile"
    folElem.save()


def coachRegister(user, form):
    coach_profile = CoachAccount(profile=user.profile)
    coach_profile.school = form["coachSchool"]
    coach_profile.French_level = form["Frenchlevel"]
    coach_profile.English_level = form["Englishlevel"]
    coach_profile.Dutch_level = form["Dutchlevel"]
    coach_profile.IBAN = form["IBAN"]
    coach_profile.nationalRegisterID = form["NationalRegisterNumber"]

    coach_profile.save()


def getUser(token):
    for user in User.objects.all():
        if user.profile.secret_key == token:
            return user
    return None
