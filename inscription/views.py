from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.urls import reverse
from django.core.mail import send_mail

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

from datetime import date
import secrets

from cad.settings import EMAIL_HOST_USER
from default.models import Mail
from users.models import Profile, Notification, studentRequest
from inscription import utils


def registerStudentView(request):
    if request.method != "POST":
        return render(request, "inscriptionStudent.html", locals())
    else:
        return registerBase(request)


def registerCoachView(request):
    if request.method != "POST":

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

        return render(request, "inscriptionCoach.html", locals())
    else:
        return registerBase(request)


def registerBase(request):
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
            utils.studentRegister(user, form)
        elif profile.account_type == "Coach":
            utils.coachRegister(user, form)

        author = "L'équipe CAD"
        title = "Bienvenue parmis nous !"
        content = "Au nom de toute l'équipe de CAD, \
            nous vous souhaitons la bienvenue ! \
            N'oubliez pas que vous pouvez nous contacter \
            si vous avez le moindre soucis via ce \
            <a href='/contact/'>formulaire</a> !"

        utils.create_notif(user, title, content, author)

        mail = Mail.objects.get(id=1)
        send_mail(
            mail.clean_header, mail.formatted_content(user), EMAIL_HOST_USER,
            [email])

        user = authenticate(
            username=user.username, password=form["passwd"])
        if user:
            login(request, user)

    except Exception as e:
        print("Error creating an account :", e)
        username = form["lastName"] + "_" + form['firstName']
        usr = User.objects.get(username=username)
        usr.delete()
        messages.add_message(
            request, messages.WARNING,
            "Il y a eu une erreur lors de la création de votre compte,\
            réessayez plus tard")
        return HttpResponseRedirect('/')

    messages.add_message(
        request, messages.SUCCESS,
        "Votre compte a bien été créé !")
    return HttpResponseRedirect('/')


@login_required(login_url='/connexion/')
def confirmation(request, string=""):
    user = utils.getUser(string)
    # token manquant ou non valide
    if string == "" or user is None:
        return HttpResponseRedirect(reverse("Error_view"))

    # Si la personne qui confirme le compte
    # n'est pas l'utilisateur concerné
    if user.username != request.user.username:
        return HttpResponseRedirect(reverse("Error_view"))

    # Si le compte est déjà confirmé,
    # l'utilisateur ne doit plus accéder à cette page
    if user.profile.verifiedAccount:
        messages.add_message(
            request, messages.WARNING,
            "Vous avez déjà confirmé votre compte !")
        return HttpResponseRedirect("/")

    # L'utilisateur a vérifié son adresse mail
    # => Compte vérifié mais pas confirmé
    profile = user.profile

    profile.verifiedAccount = True
    profile.save()

    if profile.account_type == "Etudiant":
        mail = Mail.objects.get(role='b')
        send_mail(
            mail.clean_header, mail.formatted_content(user), EMAIL_HOST_USER,
            [user.email])
        return HttpResponseRedirect(reverse("paymentView"))
    else:
        messages.add_message(
            request, messages.SUCCESS,
            "Votre compte à bien été confirmé ! Vous \
            allez pouvoir commencer à donner cours !")
        return HttpResponseRedirect("/")


def paymentView(request):
    user = request.user
    return render(request, "payment.html", locals())


def pay_later(request):
    user = request.user

    # token manquant ou non valide
    if user is None:
        return HttpResponseRedirect(reverse("Error_view"))

    # Si le compte est déjà confirmé,
    # l'utilisateur ne doit plus accéder à cette page
    if user.profile.confirmed_account:
        return HttpResponseRedirect(reverse("Error_view"))

    newNotif = Notification(user=user)
    newNotif.author = "L'équipe CAD"
    newNotif.title = "Paiement en attente"
    newNotif.content = "N'oubliez pas de <a href='/connexion/payment\
        /'>payer</a> vos cours ! Nous vous enverrons un rappel\
        dans 2 jours si nous n'avons rien reçu d'ici là"
    newNotif.save()
    user.profile.save()

    messages.add_message(
        request, messages.WARNING,
        "Votre paiement a été annulé, n'oubliez pas \
        de le compléter au plus vite, afin de pouvoir commencer a suivre des \
        cours avec nos coaches !")

    return HttpResponseRedirect("/")


def thanks(request):
    user = request.user

    # token manquant ou non valide
    if user is None or user.profile.account_type != "Etudiant":
        return HttpResponseRedirect(reverse("Error_view"))

    # Si le compte est déjà confirmé, l'utilisateur ne doit plus accéder
    # à cette page
    if user.profile.studentaccount.confirmedAccount:
        return HttpResponseRedirect(reverse("Error_view"))

    # L'utilisateur a confirmé son compte
    # Compte vérifié et confirmé
    studa = user.profile.studentaccount
    studa.confirmedAccount = True
    studa.save()

    newRequest = studentRequest(student=user)
    newRequest.save()

    utils.sendNotifToCoaches(user.profile)

    messages.add_message(
        request, messages.SUCCESS,
        "Merci d'avoir complété votre inscription ! \
        Nous allons de ce pas chercher un coach pour vous !")
    return HttpResponseRedirect("/")
