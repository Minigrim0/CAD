import logging
import hashlib

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from cad.settings import DEBUG, EMAIL_HOST_USER
from default.models import Mail
from inscription import utils
from users.models import Notification, Profile, studentRequest


def registerStudentView(request):
    """registerStudentView
        allows the student to register

    Args:
        request (request): The request object needed by all views

    Returns:
        render: the rendered student registration page
        HttpResponseRedirect: A redirection to the registration view, with all the informations needed
    """
    view_title = "Inscritpion - Etudiant"
    return render(request, "inscriptionStudent.html", locals())


def registerCoachView(request):
    """registerCoachView
        allows the coach to register

    Args:
        request (request): The request object needed by all views

    Returns:
        render: the rendered coach registration page
        HttpResponseRedirect: A redirection to the registration view, with all the informations needed
    """
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

    view_title = "Inscription - Coach"
    return render(request, "inscriptionCoach.html", locals())


def registerBase(request):
    """registerBase
        Reigsters a profile corresponding to the given informations
        (those informations are shared between the coach and the student accounts)

    Args:
        request (request): The request object needed by all views

    Returns:
        HttpResponseRedirect: A redirection to the home page, wether the user could be registered or not,
        with a message telling him if everything went well
    """

    form = request.POST

    if User.objects.filter(email=form["mailAddress"]).count() > 0:
        messages.error(request, "Un compte avec la même adresse mail existe déjà!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    username = form["lastName"] + "_" + form['firstName']
    if User.objects.filter(username=username).count() > 0:
        messages.error(request, "Un compte à ce nom existe déjà!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    email = form["mailAddress"]
    password = form["passwd"]
    user = User.objects.create(username=username, email=email)
    user.set_password(password)
    user.first_name = form["firstName"]
    user.last_name = form["lastName"]
    user.save()

    profile = Profile(user=user)
    profile.phone_number = form["PhoneNumber"]
    profile.account_type = form['accountType']
    profile.address = form["Address"]
    profile.birthDate = form["birthday"]

    for course in ["Maths", "Chimie", "Physique", "Francais"]:
        if f"Course_{course}" in form.keys():
            exec("profile." + course + "_course = True")

    profile.secret_key = hashlib.sha256(username.encode("utf-8")).hexdigest()
    profile.verifiedAccount = False
    profile.school_level = form["schoolLevel"]

    profile.save()
    if profile.account_type == "Etudiant":
        utils.studentRegister(user, form)
    elif profile.account_type == "Coach":
        utils.coachRegister(user, form)

    author = "L'équipe CAD"
    title = "Bienvenue parmi nous!"
    content = "Au nom de toute l'équipe de CAD, \
        nous vous souhaitons la bienvenue! \
        N'oubliez pas que vous pouvez nous contacter \
        si vous avez le moindre soucis via ce \
        <a href='/contact/'>formulaire</a>!"

    utils.create_notif(user, title, content, author)

    mail = Mail.objects.get(id=1)
    if not DEBUG:
        send_mail(
            mail.clean_header, mail.formatted_content(user),
            EMAIL_HOST_USER, [email])
    else:
        messages.warning(request, "L'envoi d'email est désactivé sur cette platforme!")

    user = authenticate(
        username=user.username, password=form["passwd"])
    if user:
        login(request, user)

    messages.add_message(
        request, messages.SUCCESS,
        "Votre compte a bien été créé!")
    return HttpResponseRedirect(reverse("home"))


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
            "Vous avez déjà confirmé votre compte!")
        return HttpResponseRedirect(reverse("home"))

    # L'utilisateur a vérifié son adresse mail
    # => Compte vérifié mais pas confirmé
    profile = user.profile

    profile.verifiedAccount = True
    profile.save()

    if profile.account_type == "Etudiant":
        mail = Mail.objects.get(role='b')
        if not DEBUG:
            send_mail(
                mail.clean_header, mail.formatted_content(user), EMAIL_HOST_USER,
                [user.email])
        else:
            mail = Mail.objects.get(id=1)

        return HttpResponseRedirect(reverse("paymentView"))
    else:
        messages.add_message(
            request, messages.SUCCESS,
            "Votre compte à bien été confirmé! Vous \
            allez pouvoir commencer à donner cours!")
        return HttpResponseRedirect(reverse("home"))


def paymentView(request):
    user = request.user
    view_title = "Paiement"
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
        /'>payer</a> vos cours! Nous vous enverrons un rappel\
        dans 2 jours si nous n'avons rien reçu d'ici là"
    newNotif.save()
    user.profile.save()

    messages.add_message(
        request, messages.WARNING,
        "Votre paiement a été annulé, n'oubliez pas \
        de le compléter au plus vite, afin de pouvoir commencer a suivre des \
        cours avec nos coaches!")

    return HttpResponseRedirect(reverse("home"))


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
        "Merci d'avoir complété votre inscription! \
        Nous allons de ce pas chercher un coach pour vous!")
    return HttpResponseRedirect(reverse("home"))
