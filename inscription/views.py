from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from users.models import Profile, Notification, FollowElement, studentRequest
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


def getSchedule(profil, form):
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
                profil.wanted_schedule += "1/"
                profil.wanted_schedule += form[day+"Start"] + "/"
                profil.wanted_schedule += form[day+"End"] + "."
        except Exception:
            profil.wanted_schedule += "0/0/0."
    profil.save()


def studentRegister(request):
    if request.method == "POST":
        try:
            form = request.POST
            username = form["name"] + "_" + form['firstName']
            email = form["mailAddress"]
            password = form["passwd"]
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.groups.add(Group.objects.get(name="Etudiant"))
            user.first_name = form["firstName"]
            user.last_name = form["name"]
            user.save()
            profil = Profile(user=user)

            # Follow Element creation
            folElem = FollowElement(student=user)
            folElem.coach = "L'Equipe CAD"
            folElem.comments = "Inscription sur le site CAD - cours à domicile"
            folElem.save()

            profil.secret_key = secrets.token_hex(20)
            profil.wanted_schedule = ""
            profil.save()

            if "isMobileUser" not in form.keys():
                getSchedule(profil, form)
            else:
                author = "L'équipe CAD"
                title = "Profil incomplet"
                content = "N'oubliez pas de compléter votre profil "
                content += "nous communiquant vos disponibilités, "
                content += "autrement, nous ne pourront pas trouver "
                content += "des coaches adaptés."
                create_notif(user, title, content, author)

            profil.account_type = "Etudiant"
            profil.phone_number = form["tutorPhoneNumber"]
            profil.address = form["StudentAddress"]

            YMDdate = form["bday"].split("-")
            birthDate = date(int(YMDdate[0]), int(YMDdate[1]), int(YMDdate[2]))
            profil.birthDate = birthDate

            profil.school_level = form["schoolLevel"]
            profil.tutor_name = form["tutorName"]
            profil.tutor_firstName = form["tutorFirstName"]
            profil.NeedsVisit = False
            profil.NeedsVisit = form["Visit"] != "NoVisit"

            for course in ["Maths", "Chimie", "Physique", "Francais"]:
                if "Needed"+course in form.keys():
                    exec("profil." + course + "_course = True")

            author = "L'équipe CAD"
            title = "Bienvenue parmis nous !"
            content = "Au nom de toute l'équipe de CAD, "
            content += "nous vous souhaitons la bienvenue ! "
            content += "N'oubliez pas que vous pouvez nous contacter "
            content += "si vous avez le moindre soucis via ce "
            content += "<a href='/contact/'>formulaire</a> !"
            create_notif(user, title, content, author)
            profil.save()

            try:
                user = authenticate(
                    username=user.username, password=form["passwd"])
                if user:
                    login(request, user)
            except Exception as e:
                print("Error : ", e)

            # Envoyer un mail de confirmation avec comme lien,
            # studentRegister/confirm/<Token_unique>

        except Exception as e:
            print("Error creating an account :", e)
            username = form["name"] + "_" + form['firstName']
            usr = User.objects.get(username=username)
            usr.delete()
            return HttpResponseRedirect('/02/')

        return HttpResponseRedirect('/01/')
    return HttpResponseRedirect('/05/')


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
    newNotif.content = "N'oubliez pas de <a href='/connexion/payment/'>\
    payer</a> vos cours ! Nous vous enverrons un rappel dans 2 jours si \
    nous n'avons rien reçu d'ici là"
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


def coachRegister(request):
    if request.method == "POST":
        form = request.POST
        try:
            username = form["C_name"] + '_' + form['C_firstName']
            email = form["C_mailAddress"]
            password = form["C_password"]
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.groups.add(Group.objects.get(name="Coach"))
            user.first_name = form["C_firstName"]
            user.last_name = form["C_name"]
            user.save()

            profil = Profile(user=user)

            profil.account_type = "Coach"
            profil.phone_number = form["coachPhoneNumber"]
            profil.address = form["C_Address"]

            YMDdate = form["coachbday"].split("-")
            birthDate = date(int(YMDdate[0]), int(YMDdate[1]), int(YMDdate[2]))
            profil.birthDate = birthDate

            profil.school_level = form["courseLevel"]
            profil.school = form["coachSchool"]
            profil.IBAN = form["C_IBAN"]
            profil.nationalRegisterID = form["coachNationalRegister"]
            profil.confirmed_account = True

            for course in ["Maths", "Chimie", "Physique", "Francais"]:
                if "Gives"+course in form.keys():
                    exec("profil." + course + "_course = True")

            profil.French_level = form["Frenchlevel"]
            profil.English_level = form["Englishlevel"]
            profil.Dutch_level = form["Dutchlevel"]

            profil.save()
        except Exception as e:
            print("Error :", e)
            return HttpResponseRedirect("/02/")

        return HttpResponseRedirect('/01/')
    return HttpResponseRedirect('/05/')


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
