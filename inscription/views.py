import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from cad.settings import DEBUG
from default.models import Mail
from inscription import utils
from users.models import Notification, studentRequest
from users.forms import StudentRegisterForm, CoachRegisterForm


def registerStudentView(request):
    """ allows a student to register an account """

    if request.method == "POST":
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = utils.registerUser(form, "a")

            user = authenticate(
                username=user.username,
                password=form.cleaned_data["password"])
            if user:
                login(request, user)

            messages.add_message(
                request, messages.SUCCESS,
                "Votre compte a bien été créé!")
            welcomeUser(request, user, host=request.META['HTTP_HOST'])
            return HttpResponseRedirect(reverse("home"))
    else:
        form = StudentRegisterForm()

    view_title = "Inscription - Etudiant"
    return render(request, "inscription.html", locals())


def registerCoachView(request):
    """ allows a coach to register an account """
    if request.method == "POST":
        form = CoachRegisterForm(request.POST)
        if form.is_valid():
            user = utils.registerUser(form, "b")

            user = authenticate(
                username=user.username,
                password=form.cleaned_data["password"])
            if user:
                login(request, user)

            messages.add_message(
                request, messages.SUCCESS,
                "Votre compte a bien été créé!")
            welcomeUser(request, user, host=request.META['HTTP_HOST'])
            return HttpResponseRedirect(reverse("home"))
    else:
        form = CoachRegisterForm()

    view_title = "Inscription - Coach"
    return render(request, "inscription.html", locals())


def welcomeUser(request, user, host):
    """Welcomes the new user, by sending him an email and a notification

    Args:
        user (django.contrib.auth.models.User): The new user
    """

    author = "L'équipe CAD"
    title = "Bienvenue parmi nous!"
    content = "Au nom de toute l'équipe de CAD, \
        nous vous souhaitons la bienvenue! \
        N'oubliez pas que vous pouvez nous contacter \
        si vous avez le moindre souci via ce \
        <a href='/contact/'>formulaire</a>!"

    newNotif = Notification(user=user)
    newNotif.title = title
    newNotif.content = content
    newNotif.author = author
    newNotif.save()

    mail = Mail.objects.get(id=1)
    if not DEBUG:
        logging.warning("Sending mail to {}".format(user.email))

        mail.send(user, request.META["HTTP_HOST"])
    else:
        messages.warning(request, "L'envoi d'email est désactivé sur cette platforme!")


@login_required(login_url='/users/login')
def confirmation(request):
    token = request.GET.get("key", "")
    user = utils.getUser(token)
    # token manquant ou non valide
    if token == "" or user is None:
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

    if profile.account_type == "a":
        mail = Mail.objects.get(role='b')
        if not DEBUG:
            mail.send(user, request.META["HTTP_HOST"])
        else:
            mail = Mail.objects.get(id=1)

        return HttpResponseRedirect(reverse("paymentView"))
    else:
        messages.add_message(
            request, messages.SUCCESS,
            "Votre compte à bien été confirmé! Nous allons\
            bientôt entrer en contact avec vous!")
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
    if user is None or user.profile.account_type != "a":
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
