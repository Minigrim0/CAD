import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login

from administration.utils import populate_data
from .models import Notification, Transaction, studentRequest
from .utils import thanksCoaches
from .forms import StudentReadOnlyForm, BaseReadOnly, CoachReadOnlyForm


def ErrorView(request):
    messages.add_message(
        request, messages.ERROR,
        "Une erreur est survenue lors du chargement \
    de la page")
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
    a_user = request.user
    student_set = User.objects.filter(profile__studentaccount__coach=a_user)

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

        user.profile.save()

        logging.debug("Added notification (id {}) to {}".format(notif.pk, request.POST['user']))
        return HttpResponse("Success")

    return HttpResponse("failed")


@login_required
def remove_notif(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("Error_view"))

    try:
        user = User.objects.get(username=request.user.username)

        user.notification_set.get(id=request.POST["id"]).delete()
        user.profile.notifications_nb -= 1
        if user.profile.notifications_nb < 0:
            user.profile.notifications_nb = 0

        user.profile.save()
        user.save()

        return HttpResponse("success")
    except Exception as e:
        logging.critical("Error while deleting notification : {}".format(e))
        return HttpResponse("failed")


@staff_member_required
def modify_balance(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    admin = User.objects.get(username=request.POST["approver"])
    student = User.objects.get(username=request.POST["user"])
    to_add = request.POST["amout_add"]

    tran = Transaction(student=student.profile.studentaccount)
    tran.amount = to_add
    tran.admin = admin
    tran.save()

    return JsonResponse({"new_balance": student.profile.studentaccount.balance})


@login_required
def disconnect(request):
    logout(request)

    messages.add_message(
        request, messages.WARNING,
        "Vous avez été déconnecté")
    return HttpResponseRedirect(reverse("home"))


@login_required
def requestView(request, id=0):
    if id != 0:
        allowed = request.user.profile.account_type == "Coach"
        allowed = allowed or request.user.is_superuser
        if request.user.is_authenticated and allowed:
            student_request = studentRequest.objects.get(id=id)
            student_request_closed = studentRequest.objects.get(id=id)
            user = student_request.student
            coach = request.user
            coaches = [
                coach.user.username for coach in student_request.coaches.all()]

            view_title = "Requête"
            return render(request, "requests.html", locals())
        else:
            return HttpResponseRedirect(reverse("Error_view"))
    else:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                student_requests = studentRequest.objects.all().exclude(
                    is_closed=True)
                student_requests_closed = studentRequest.objects.all().exclude(
                    is_closed=False)

                view_title = "Requêtes"
                return render(request, "requestsAdmin.html", locals())
            else:
                return HttpResponseRedirect(reverse("Error_view"))
        else:
            return HttpResponseRedirect(reverse("Error_view"))


@login_required
def chooseCoach(request):
    if request.method != "POST":
        return HttpResponse("/05/")

    query = request.POST

    s_request = studentRequest.objects.get(id=query['id'])
    coach = s_request.coaches.get(user__username=query["coach"])
    other_coaches = s_request.coaches.all().exclude(
        user__username=query["coach"])

    s_request.is_closed = True
    s_request.choosenCoach = coach.user.username
    student = s_request.student.profile.studentAccount
    student.coach = coach
    ca = coach.coachaccount
    ca.nbStudents += 1

    s_request.save()
    student.save()
    coach.save()
    ca.save()

    author = "L'équipe CAD"
    title = "Félicitations!"
    content = "Vous avez été choisit pour enseigner à {} {}! Vous pouvez \
    vous rendre sur votre profil pour retrouver les coordonées de cet \
    étudiant".format(student.first_name, student.last_name)
    new_Notif = Notification(
        user=coach.user, author=author, title=title, content=content)
    new_Notif.save()

    thanksCoaches(other_coaches, student)

    return HttpResponse("success")


def requestManage(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("Error_view"))

    if request.POST["decision"] == 'true':
        student_request = studentRequest.objects.get(id=request.POST["id"])
        coach = User.objects.get(id=request.POST["coach"])
        student_request.coaches.add(coach.profile)
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

    return JsonResponse({"users" : userData})


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
