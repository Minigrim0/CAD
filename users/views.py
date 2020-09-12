import logging

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseRedirect, JsonResponse, Http404)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login

from administration.utils import populate_data
from .models import Notification, studentRequest
from .forms import StudentReadOnlyForm, BaseReadOnly, CoachReadOnlyForm


def user_home(request):
    return HttpResponseRedirect(reverse("my_account"))


def ErrorView(request):
    messages.add_message(
        request, messages.ERROR,
        "Une erreur est survenue lors du chargement de la page")
    return HttpResponseRedirect(reverse("home"))


@login_required
def userView(request):
    user = request.user
    notifications = user.notification_set.all()

    data = populate_data(user.profile.account_type, user)
    if user.profile.account_type == "a":
        form = StudentReadOnlyForm(data)
    elif user.profile.account_type == "b":
        form = CoachReadOnlyForm(data)
    else:
        data = populate_data("other", user)
        form = BaseReadOnly(data)

    view_title = "Mon compte"
    return render(request, 'user.html', locals())


@login_required
def followView(request):
    a_user = request.user
    followelement_set = a_user.followelement_set.all()

    view_title = "Mon suivi"
    return render(request, 'follow.html', locals())


@login_required
def studentsView(request):
    coach = request.user.profile.coachaccount
    student_set = User.objects.filter(profile__studentaccount__coach=coach)

    view_title = "Mes étudiants"
    return render(request, 'students.html', locals())


@login_required
def send_notif(request):
    if request.method == "POST":

        user = User.objects.get(username=request.POST['user'])
        notif = Notification()
        notif.user = user
        notif.title = request.POST["title"]
        notif.content = request.POST["content"]
        notif.author = request.POST["sender"]
        notif.save()

        logging.debug("Added notification (id {}) to {}".format(notif.pk, request.POST['user']))
        # TODO: send with a new template
        return HttpResponse("Success")

    return HttpResponse("failed")


@login_required
def remove_notif(request):
    if request.method != "POST":
        return ErrorView(request)

    user = request.user
    notification = get_object_or_404(Notification, id=request.POST["id"])
    if notification.user.username != user.username:
        raise Http404()
    notification.delete()

    return HttpResponse("success")


@login_required
def disconnect(request):
    logout(request)

    messages.add_message(
        request, messages.WARNING,
        "Vous avez été déconnecté")
    return HttpResponseRedirect(reverse("home"))


@login_required
def requestView(request):
    request_id = request.GET.get('id', 0)

    allowed = request.user.profile.account_type == "b"
    if request.user.is_authenticated and allowed:
        student_request = studentRequest.objects.get(id=request_id)
        student_request_closed = studentRequest.objects.get(id=request_id)
        user = student_request.student
        coach = request.user
        coaches = [
            coach.profile.user.username for coach in student_request.coaches.all()]

        view_title = "Requête"
        return render(request, "requests.html", locals())
    else:
        return ErrorView(request)


@login_required
def acceptRequest(request):
    if request.method != "POST":
        return ErrorView(request)

    if request.POST["decision"] == 'true':
        student_request = studentRequest.objects.get(id=request.POST["id"])
        coach = User.objects.get(id=request.POST["coach"])
        student_request.coaches.add(coach.profile.coachaccount)
        student_request.save()
        return HttpResponse("A été ajouté")

    return HttpResponse("N'a pas été ajouté")


def get_users(request):
    """
        returns the users linked to the email provided
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method : Requets must be type POST")

    email = request.POST.get("email", "")
    users = User.objects.filter(email=email)

    userData = []
    for user in users:
        userData.append(
            ("{} {}".format(user.first_name, user.last_name), user.username)
        )

    return JsonResponse({"users": userData})


def login_view(request):
    """
        Allows a user to connect to his account
    """
    if request.method != "POST":
        view_title = "Connectez vous"
        return render(request, 'connexion.html', locals())

    form = request.POST
    username = form["username"]
    password = form["password"]

    authuser = authenticate(username=username, password=password)
    if authuser:
        login(request, authuser)
        messages.add_message(
            request, messages.SUCCESS,
            "Rebonjour {}".format(request.user.first_name))
    else:
        messages.add_message(
            request, messages.ERROR,
            "Vos identifiants ne correspondent à aucun compte!")

    # If the user could not connect, redirect him to the login page again
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login_view"))

    next = request.GET.get("next", "")
    if next != "":
        return HttpResponseRedirect(next)
    return HttpResponseRedirect(reverse("home"))
