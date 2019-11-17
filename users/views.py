from django.shortcuts import render
from django.http import HttpResponse,\
    HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from users.models import Notification, studentRequest, Transaction


def ErrorView(request):
    messages.add_message(
        request, messages.ERROR,
        "Une erreur est survenue lors du chargement \
    de la page")
    return HttpResponseRedirect("/")


@login_required(login_url='/connexion/')
def userView(request):
    user = request.user
    notifications = user.notification_set.all()
    nb_notifs = user.notification_set.count()

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

    return render(request, 'user.html', locals())


@login_required(login_url='/connexion/')
def followView(request):
    a_user = request.user
    followelement_set = a_user.followelement_set.all()

    return render(request, 'follow.html', locals())


@login_required(redirect_field_name='/05/')
def studentsView(request):
    return render(request, 'students.html', locals())


@login_required
def send_notif(request):
    # Sends a notification to a user
    if request.method == "POST":

        user = User.objects.get(username=request.POST['user'])
        _notif = Notification()
        _notif.user = user
        _notif.title = request.POST["title"]
        _notif.content = request.POST["content"]
        _notif.author = request.POST["sender"]
        _notif.save()

        user.profile.save()

        print("Added notification to", request.POST['user'])
        return HttpResponse("Success")

    return HttpResponse("failed")


@login_required
def remove_notif(request):
    if request.method == "POST":
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
            print("Error :", e)
            return HttpResponse("failed")

    return HttpResponseRedirect("/05/")


@login_required(redirect_field_name='/05/')
def disconnect(request):
    logout(request)
    return HttpResponseRedirect("/06/")


@login_required(redirect_field_name='/05/')
def requestView(request, id=0):
    if id != 0:
        allowed = request.user.profile.account_type == "Coach"
        allowed = allowed or request.user.is_superuser
        if request.user.is_authenticated() and allowed:
            student_request = studentRequest.objects.get(id=id)
            student_request_closed = studentRequest.objects.get(id=id)
            user = student_request.student
            coach = request.user
            coaches = [
                coach.user.username for coach in student_request.coaches.all()]

            return render(request, "requests.html", locals())
        else:
            return HttpResponseRedirect(reverse("Error_view"))
    else:
        if request.user.is_authenticated():
            if request.user.is_superuser:
                student_requests = studentRequest.objects.all().exclude(
                    is_closed=True)
                student_requests_closed = studentRequest.objects.all().exclude(
                    is_closed=False)

                return render(request, "requestsAdmin.html", locals())
            else:
                return HttpResponseRedirect(reverse("Error_view"))
        else:
            return HttpResponseRedirect(reverse("Error_view"))


def thanksCoaches(coaches, student):
    author = "L'équipe CAD"
    title = "Merci d'avoir répondu présent"
    content = "Merci d'avoir répondu présent à la requête de {} {}. \
    Malheureusement, vous n'avez pas été choisit pour donner cours à \
    cet étudiant. Mais ne vous en faites pas, voitre tour viendra !".format(
        student.first_name, student.last_name)
    for coach in coaches:
        new_notif = Notification(
            user=coach.user,
            author=author,
            title=title,
            content=content)
        new_notif.save()


@login_required(redirect_field_name='/05/')
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
    student = s_request.student
    student.coach = coach
    ca = coach.coachaccount
    ca.nbStudents += 1

    s_request.save()
    student.save()
    coach.save()
    ca.save()

    author = "L'équipe CAD"
    title = "Félicitations !"
    content = "Vous avez été choisit pour enseigner à {} {} ! Vous pouvez \
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
