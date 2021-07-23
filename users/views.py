from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
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
    followelement_set = FollowElement.objects.filter(  # skipcq PYL-W0641
        coach=request.user).order_by("-date", "-endHour")

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
            messages.success(
                request, "Le cours a bien été ajouté !"
            )
            return HttpResponseRedirect(reverse("my_students"))
    else:
        form = addFollowElementForm()

    view_title = "Ajouter un cours"  # skipcq PYL-W0641
    return render(request, "addFollow.html", locals())


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
