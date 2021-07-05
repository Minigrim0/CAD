from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from default.models import Mail
from inscription import utils
from users.models import Notification, StudentRequest
from users.forms import StudentRegisterForm, CoachRegisterForm

from inscription.decorators import mustnt_be_logged_in


@mustnt_be_logged_in(action="inscrire")
def registerUserView(request):
    """The view allowing a user to register as either a coach or a student

    Raises:
        HttpResponseBadRequest: In case the GET parameter specifying the type of account isn't correct

    Returns:
        render: The render of the register template in case the request method was 'GET' or the user
        could not successfully register
        redirect: a redirection to the home page if the user sucessfully registered
    """

    userType = request.GET.get("type", "a")
    if userType not in "ab":
        raise HttpResponseBadRequest("Le type de compte est invalide")

    if request.method == "POST":
        form = (
            StudentRegisterForm(request.POST)
            if userType == "a"
            else CoachRegisterForm(request.POST)
        )

        if form.is_valid():
            user = utils.registerUser(form, userType)
            user = authenticate(
                username=user.username, password=form.cleaned_data["password"]
            )
            if user:
                login(request, user)

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Votre compte a bien été créé! Consultez votre boite mail pour confirmer votre compte.",
                )
                utils.welcomeUser(request, user)
                return HttpResponseRedirect(reverse("home"))
    else:
        form = StudentRegisterForm() if userType == "a" else CoachRegisterForm()

    view_title = "Inscription - Etudiant" if userType == "a" else "Inscription - Coach"

    return render(request, "inscription.html", locals())


@login_required
def confirmation_view(request):
    """A view to verify the email address of the user

    Args:
        request (request): request object needed by all the views

    Returns:
        [type]: [description]
    """
    token = request.GET.get("key", "")
    user = utils.getUser(token)
    # token manquant ou non valide
    if token == "" or user is None:
        return HttpResponseRedirect(reverse("Error_view"))

    # Si le compte est déjà confirmé,
    # l'utilisateur ne doit plus accéder à cette page
    if user.profile.verifiedAccount:
        messages.add_message(
            request, messages.WARNING, "Vous avez déjà confirmé votre compte!"
        )
        return HttpResponseRedirect(reverse("home"))

    # L'utilisateur a vérifié son adresse mail
    # => Compte vérifié mais pas confirmé
    profile = user.profile

    profile.verifiedAccount = True
    profile.save()

    if profile.account_type == "a":
        mail = Mail.objects.get(role="b")
        mail.send(user)

        return HttpResponseRedirect(reverse("paymentView"))
    messages.add_message(
        request,
        messages.SUCCESS,
        "Votre compte à bien été confirmé! Nous allons\
        bientôt entrer en contact avec vous!",
    )
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
        request,
        messages.WARNING,
        "Votre paiement a été annulé, n'oubliez pas \
        de le compléter au plus vite, afin de pouvoir commencer a suivre des \
        cours avec nos coaches!",
    )

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

    StudentRequest.objects.create(student=user)

    utils.sendNotifToCoaches(user.profile)

    messages.add_message(
        request,
        messages.SUCCESS,
        "Merci d'avoir complété votre inscription! \
        Nous allons de ce pas chercher un coach pour vous!",
    )
    return HttpResponseRedirect(reverse("home"))
