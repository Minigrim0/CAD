from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from users.models import Profile, Notification, FollowElement, studentRequest
from datetime import date
import secrets

# INFO CODES
# 01 -> Register Success
# 02 -> Register Failed
# 03 -> Connexion Success
# 04 -> Connexion Failed
# 05 -> Not a post Error
# 06 -> successfully disconnected
# 07 -> User successfully deleted
# 08 -> Message sent
# 09 -> Message failed
# 10 -> Payment annulation
# 11 -> Payment received
# 12 -> Suspended account
# 13 -> Confirmed account


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
            if "isMobileUser" not in form.keys():
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
            else:
                newNotif = Notification(user=user)
                newNotif.author = "L'équipe CAD"
                newNotif.title = "Profil incomplet"
                newNotif.content = "N'oubliez pas de compléter votre profil "
                newNotif.content += "nous communiquant vos disponibilités, "
                newNotif.content += "autrement, nous ne pourront pas trouver "
                newNotif.content += "des coaches adaptés."
                newNotif.save()
                profil.notifications_nb += 1

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
            if form["Visit"] != "NoVisit":
                profil.NeedsVisit = True

            for course in ["Maths", "Chimie", "Physique", "Francais"]:
                if "Needed"+course in form.keys():
                    exec("profil." + course + "_course = True")

            newNotif = Notification(user=user)
            newNotif.author = "L'équipe CAD"
            newNotif.title = "Bienvenue parmis nous !"
            newNotif.content = "Au nom de toute l'équipe de CAD, "
            newNotif.content += "nous vous souhaitons la bienvenue ! "
            newNotif.content += "N'oubliez pas que vous pouvez nous contacter "
            newNotif.content += "si vous avez le moindre soucis via ce "
            newNotif.content += "<a href='/contact/'>formulaire</a> !"
            newNotif.save()
            profil.notifications_nb += 1
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
    user.profile.verified_account = True
    user.profile.save()

    if user.profile.account_type == "Etudiant":
        return render(request, 'default/payment.html', locals())
    else:
        user.profile.confirmed_account = True
        user.profile.save()
        return HttpResponseRedirect("/13/")


def pay_later(request, string=""):
    user = getUser(string)

    # token manquant ou non valide
    if string == "" or user is None:
        return HttpResponseRedirect("/05/")

    # Si le compte est déjà confirmé,
    # l'utilisateur ne doit plus accéder à cette page
    if user.profile.confirmed_account:
        return HttpResponseRedirect("/05/")

    newNotif = Notification(user=user)
    newNotif.author = "L'équipe CAD"
    newNotif.title = "Paiement en attente"
    newNotif.content = "N'oubliez pas de payer vos cours !"
    newNotif.content += "Nous vous enverrons un rappel dans 2 jours si nous "
    newNotif.content += "n'avons rien reçu d'ici là"
    newNotif.save()
    user.profil.notifications_nb += 1
    user.profil.save()

    return HttpResponseRedirect("/10/")


def thanks(request, string=""):
    user = getUser(string)

    # token manquant ou non valide
    if string == "" or user is None:
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

    return HttpResponse("/11/")


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
        maths_bool = coach.Maths_course == student.Maths_course
        chimie_bool = coach.Chimie_course == student.Chimie_course
        physique_bool = coach.Physique_course == student.Physique_course
        francais_bool = coach.Francais_course == student.Francais_course
        compatible = maths_bool
        compatible = compatible or chimie_bool
        compatible = compatible or physique_bool
        compatible = compatible or francais_bool
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
                str(student.user.studentrequest.id))
            newNotif.content += "pour voir le profil de l'etudiant"
            newNotif.save()
            coach.notifications_nb += 1
            coach.save()
