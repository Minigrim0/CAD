from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from users.models import Profile, Notification, FollowElement, studentRequest, StudentAccount, CoachAccount
from datetime import date
import secrets


def connexion(request):
    i_day = {
        'Monday': 'Lundi',
        'Tuesday': 'Mardi',
        'Wednesday': 'Mercredi',
        'Thursday': 'Jeudi',
        'Friday': 'Vendredi',
        'Saturday': 'Samedi',
        'Sunday': 'Dimanche'}

    i_langLevel = {
        '5': 'Langue maternelle',
        '4': 'Très bon',
        '3': 'Bon',
        '2': 'Notions de base',
        '1': 'Aucun'}

    i_lang = {
        'French': 'Francais',
        'Dutch': 'Néerlandais',
        'English': 'Anglais'}

    return render(request, 'default/connexion.html', locals())


def connect(request):
    if request.method == "POST":
        form = request.POST

        email = form["coMail"]
        password = form["coPass"]

        try:
            user = User.objects.get(email=email)  # Get user obj via its email
            user = authenticate(username=user.username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect("/03/")
        except Exception as e:
            print("Error : ", e)

        return HttpResponseRedirect("/04/")

    else:
        return HttpResponseRedirect('/05/')


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


def createStudentProfile(user, form):

    student_profile = StudentAccount(profile=user.profile)

    student_profile.tutor_name = form["tutorLastName"]
    student_profile.tutor_firstName = form["tutorFirstName"]
    student_profile.NeedsVisit = form["Visit"] != "NoVisit"
    student_profile.comments = form["comments"]
    student_profile.wanted_schedule = ""
    student_profile.save()

    if "isMobileUser" not in form.keys():
        getSchedule(student_profile, form)
    else:
        author = "L'équipe CAD"
        title = "Profil incomplet"
        content = "N'oubliez pas de compléter votre profil \
            en nous communiquant vos disponibilités, \
            autrement, nous ne pourront pas trouver \
            des coaches adaptés."
        create_notif(user, title, content, author)

    author = "L'équipe CAD"
    title = "Bienvenue parmis nous !"
    content = "Au nom de toute l'équipe de CAD, \
        nous vous souhaitons la bienvenue ! \
        N'oubliez pas que vous pouvez nous contacter \
        si vous avez le moindre soucis via ce \
        <a href='/contact/'>formulaire</a> !"

    create_notif(user, title, content, author)
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


def register(request):
    if request.method != "POST":
        return HttpResponseRedirect('/05/')
    try:
        form = request.POST
        username = form["lastName"] + "_" + form['firstName']
        email = form["mailAddress"]
        password = form["passwd"]
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.groups.add(Group.objects.get(name=form["accountType"]))
        user.first_name = form["firstName"]
        user.last_name = form["lastName"]
        user.save()

        profile = Profile(user=user)
        profile.phone_number = form["PhoneNumber"]
        profile.account_type = form['accountType']
        profile.address = form["Address"]
        YMDdate = form["birthday"].split("-")
        birthDate = date(int(YMDdate[0]), int(YMDdate[1]), int(YMDdate[2]))
        profile.birthDate = birthDate

        for course in ["Maths", "Chimie", "Physique", "Francais"]:
            if "Course_"+course in form.keys():
                exec("profile." + course + "_course = True")

        profile.secret_key = secrets.token_hex(20)
        profile.verifiedAccount = False
        profile.school_level = form["schoolLevel"]

        profile.save()
        if profile.account_type == "Etudiant":
            createStudentProfile(user, form)
        elif profile.account_type == "Coach":
            coachRegister(user, form)

        # Envoyer un mail de confirmation avec comme lien,
        # studentRegister/confirm/<Token_unique>

        try:  # Try to connect the student directly
            user = authenticate(
                username=user.username, password=form["passwd"])
            if user:
                login(request, user)
        except Exception as e:
            print("Error : ", e)

    except Exception as e:
        print("Error creating an account :", e)
        username = form["lastName"] + "_" + form['firstName']
        usr = User.objects.get(username=username)
        usr.delete()
        return HttpResponseRedirect('/02/')

    return HttpResponseRedirect('/01/')


def confirmation(request, string=""):
    user = getUser(string)
    # token manquant ou non valide
    if string == "" or user is None:
        return HttpResponseRedirect("/05/")

    # Si le compte est déjà confirmé,
    # l'utilisateur ne doit plus accéder à cette page
    if user.profile.confirmed_account:
        return HttpResponseRedirect("/05/")

    # L'utilisateur a vérifié son adresse mail
    # Compte vérifié mais pas confirmé
    profile = user.profile

    profile.verified_account = True
    profile.save()

    if profile.account_type == "Etudiant":
        return render(request, 'default/payment.html', locals())
    else:
        profile.confirmed_account = True
        profile.save()
        return HttpResponseRedirect("/13/")


def paymentView(request):
    user = request.user
    return render(request, "default/payment.html", locals())


def pay_later(request):
    user = request.user

    # token manquant ou non valide
    if user is None:
        return HttpResponseRedirect("/05/")

    # Si le compte est déjà confirmé,
    # l'utilisateur ne doit plus accéder à cette page
    if user.profile.confirmed_account:
        return HttpResponseRedirect("/05/")

    newNotif = Notification(user=user)
    newNotif.author = "L'équipe CAD"
    newNotif.title = "Paiement en attente"
    newNotif.content = "N'oubliez pas de <a href='/connexion/payment\
        /'>payer</a> vos cours ! Nous vous enverrons un rappel\
        dans 2 jours si nous n'avons rien reçu d'ici là"
    newNotif.save()
    user.profile.save()

    return HttpResponseRedirect("/10/")


def thanks(request):
    user = request.user

    # token manquant ou non valide
    if user is None:
        return HttpResponseRedirect("/05/")

    # Si le compte est déjà confirmé, l'utilisateur ne doit plus accéder
    # à cette page
    if user.profile.confirmed_account:
        return HttpResponseRedirect("/05/")

    # L'utilisateur a confirmé son compte
    # Compte vérifié et confirmé
    user.profile.confirmed_account = True
    user.profile.save()

    newRequest = studentRequest(student=user)
    newRequest.save()

    sendNotifToCoaches(user.profile)

    return HttpResponseRedirect("/11/")


def getUser(token):
    for user in User.objects.all():
        if user.profile.secret_key == token:
            return user
    return None


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
        else:
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
