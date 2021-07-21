import logging

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    JsonResponse,
    Http404,
)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login

from administration.utils import populate_data
from users.models import Notification, StudentRequest, StudentAccount, FollowElement
from users.forms import (
    StudentReadOnlyForm,
    BaseReadOnly,
    CoachReadOnlyForm,
    addFollowElementForm,
)
from inscription.decorators import mustnt_be_logged_in
from inscription.utils import send_confirmation_mail


def user_home(request) -> HttpResponseRedirect:
    """Redirects to the user home page"""
    return HttpResponseRedirect(reverse("my_account"))


def ErrorView(request) -> HttpResponseRedirect:
    """Adds an error messages and redirects to the home page"""
    messages.add_message(
        request, messages.ERROR, "Une erreur est survenue lors du chargement de la page"
    )
    return HttpResponseRedirect(reverse("home"))


@login_required
def userView(request) -> HttpResponse:
    """Renders the home page of the user

    Returns:
        HttpResponse: The rendered template of the user's home page
    """
    user = request.user
    notifications = user.notification_set.all().order_by("-date_created")  # skipcq PYL-W0641

    data = populate_data(user.profile.account_type, user)
    if user.profile.account_type == "a":
        form = StudentReadOnlyForm(data)  # skipcq PYL-W0641
    elif user.profile.account_type == "b":
        form = CoachReadOnlyForm(data)
    else:
        data = populate_data("other", user)
        form = BaseReadOnly(data)

    view_title = "Mon compte"  # skipcq PYL-W0641
    return render(request, "user.html", locals())


@login_required
def followView(request) -> HttpResponse:
    """Shows the diffrent courses a student has attended to"""
    a_user = request.user
    followelement_set = a_user.followelement_set.all()  # skipcq PYL-W0641

    view_title = "Mon suivi"  # skipcq PYL-W0641
    return render(request, "follow.html", locals())


@login_required
def studentsView(request):
    """Shows the students of a coach"""
    coach = request.user.profile.coachaccount
    student_set = coach.students.all()  # skipcq PYL-W0641

    view_title = "Mes étudiants"  # skipcq PYL-W0641
    return render(request, "students.html", locals())


@login_required
def addFollowElement(request) -> HttpResponse:
    """Creates a new follow element or displays the form to do it"""
    student_pk = request.GET.get("pk", -1)
    student = get_object_or_404(StudentAccount, pk=student_pk)

    if request.method == "POST":
        form = addFollowElementForm(request.POST)
        if form.is_valid():
            course = FollowElement.objects.create(
                coach=request.user, student=student.profile.user
            )
            course.date = form.cleaned_data["date"]
            course.startHour = form.cleaned_data["startHour"]
            course.endHour = form.cleaned_data["endHour"]
            course.comments = form.cleaned_data["comments"]
            course.save()
            return HttpResponseRedirect(reverse("my_students"))
    else:
        form = addFollowElementForm()

    view_title = "Ajouter un cours"  # skipcq PYL-W0641
    return render(request, "addFollow.html", locals())


@login_required
def send_notif(request) -> HttpResponse:
    """Sends a notification to the concerned user

    Returns:
        HttpResponse: A small message indicating the status of the request
    """
    if request.method == "POST":
        user = User.objects.get(username=request.POST["user"])
        notif = Notification()
        notif.user = user
        notif.title = request.POST["title"]
        notif.content = request.POST["content"]
        notif.author = request.POST["sender"]
        notif.save()
        notif.send_as_mail()

        logging.debug(
            "Added notification (id {}) to {}".format(notif.pk, request.POST["user"])
        )

        return HttpResponse("Success")

    return HttpResponse("failed")


@login_required
def remove_notif(request) -> HttpResponse:
    """Removes a notification

    Raises:
        Http404: In case the notification doesn't exist

    Returns:
        HttpResponse: A message indicating the request went well
    """
    if request.method != "POST":
        return ErrorView(request)

    user = request.user
    notification = get_object_or_404(Notification, id=request.POST["id"])
    if notification.user.username != user.username:
        raise Http404()
    notification.delete()

    return HttpResponse("success")


@login_required
def disconnect(request) -> HttpResponseRedirect:
    """Disconnects the user

    Returns:
        HttpResponseRedirect: A redirection to the home page
    """
    logout(request)

    messages.add_message(request, messages.WARNING, "Vous avez été déconnecté")
    return HttpResponseRedirect(reverse("home"))


@login_required
def requestView(request) -> HttpResponse:
    """Shows a request to a coach

    Returns:
        HttpReponse: The request page or an error if the user cannot access the page
    """
    request_id = request.GET.get("id", 0)

    if request.user.profile.account_type == "b":
        student_request = StudentRequest.objects.get(id=request_id)
        student = student_request.student  # skipcq PYL-W0641
        coaches = [  # skipcq PYL-W0641
            coach.profile.user.username for coach in student_request.coaches.all()
        ]
        coach = request.user

        coach_schedule = coach.profile.coachaccount.schedule(student_request)  # skipcq PYL-W0641

        view_title = "Requête"  # skipcq PYL-W0641
        return render(request, "requests.html", locals())
    return ErrorView(request)


@login_required
def acceptRequest(request) -> HttpResponse:
    """Accepts the request given as post parameter

    Returns:
        HttpResponse: A message indicating the request went well
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method : Request must type be 'POST'")

    accepted = request.POST.get("decision", False) == "true"
    coachschedule = request.POST.get("schedule", "")

    student_request = get_object_or_404(StudentRequest, id=request.POST["id"])
    coach = get_object_or_404(User, id=request.POST["coach"])
    student_request.coaches.add(coach.profile.coachaccount)
    student_request.save()

    throughmodel = student_request.coachrequestthrough_set.get(
        coach=coach.profile.coachaccount
    )
    throughmodel.has_accepted = accepted
    throughmodel.coachschedule = coachschedule
    throughmodel.save()

    return HttpResponse("Success")


def get_users(request) -> JsonResponse:
    """Returns the users linked to the email provided

    Returns:
        JsonResponse: a dictionnary containing the name of the users with the given email address
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method : Request type must be 'POST'")

    email = request.POST.get("email", "")
    users = User.objects.filter(email=email)

    userData = []
    for user in users:
        userData.append(
            ("{} {}".format(user.first_name, user.last_name), user.username)
        )

    return JsonResponse({"users": userData})


@mustnt_be_logged_in(action="connecter")
def login_view(request):
    """Allows a user to connect to his account"""
    if request.method != "POST":
        view_title = "Connectez vous"  # skipcq PYL-W0641
        return render(request, "connexion.html", locals())

    form = request.POST
    username = form["username"]
    password = form["password"]

    authuser = authenticate(username=username, password=password)
    if authuser:
        login(request, authuser)
        messages.add_message(
            request, messages.SUCCESS, "Rebonjour {}".format(request.user.first_name)
        )
    else:
        messages.add_message(
            request, messages.ERROR, "Vos identifiants ne correspondent à aucun compte!"
        )

    # If the user could not connect, redirect him to the login page again
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login_view"))

    nextPage = request.GET.get("next", "")
    if nextPage != "":
        return HttpResponseRedirect(nextPage)
    return HttpResponseRedirect(reverse("home"))


@login_required
def send_confirmation_email(request):
    """Resends a confirmation email in case the user didn't receive the confirmation email"""
    if request.user.profile.verifiedAccount:
        messages.add_message(
            request, messages.ERROR, "Vous avez déjà confirmé votre adresse mail !"
        )

    send_confirmation_mail(request.user)
    messages.add_message(
        request, messages.SUCCESS, "Un nouvel email de vérification a été envoyé, "
        "n'oubliez pas de vérifier les spams !"
    )
    return HttpResponseRedirect(reverse("home"))
