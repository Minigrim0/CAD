from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from administration.views import serializeDate
from users.models import Notification, studentRequest, Profile


def userView(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/05/")

    a_user = request.user

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

    notifications = a_user.notification_set.all()
    nb_notifs = a_user.notification_set.count()

    return render(request, 'users/user.html', locals())


def followView(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/05/")

    a_user = request.user
    followelement_set = a_user.followelement_set.all()

    return render(request, 'users/follow.html', locals())


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
        user.profile.notifications_nb += 1

        user.profile.save()

        print("Added notification to", request.POST['user'])
        return HttpResponse("Success")

    return HttpResponse("failed")


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


def disconnect(request):
    logout(request)
    return HttpResponseRedirect("/06/")


def ModifyDays(profile, form):
    profile.wanted_schedule = ""
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
                profile.wanted_schedule += "1/"
                profile.wanted_schedule += form[day+"Start"] + "/"
                profile.wanted_schedule += form[day+"End"] + "."
        except KeyError:
            profile.wanted_schedule += "0/0/0."
    profile.save()


def ModifyStudent(profile, form):
    ModifyDays(profile, form)

    profile.NeedsVisit = False
    if form["Visit"] != "NoVisit":
        profile.NeedsVisit = True

    profile.comments = form["comments"]

    profile.tutor_firstName = form["tutorFirstName"]
    profile.tutor_name = form["tutorName"]
    profile.save()


def ModifyCoach(profile, form):
    profile.school = form["school"]
    profile.IBAN = form["IBAN"]
    profile.nationalRegisterID = form["natRegID"]
    profile.French_level = form["Frenchlevel"]
    profile.English_level = form["Englishlevel"]
    profile.Dutch_level = form["Dutchlevel"]

    profile.save()


def modifyUser(request):
    if request.method == "POST":
        try:
            form = request.POST
            if "delete" in form.keys():
                usr = User.objects.get(username=form["username"])
                usr.is_active = False
                usr.save()
                logout(request)
                return HttpResponseRedirect("/12/")

            usr = User.objects.get(username=form["username"])
            usr.first_name = form["firstName"]
            usr.last_name = form["lastName"]
            usr.email = form["mail"]
            usr.save()
            profile = usr.profile

            try:
                type = usr.profile.account_type
            except Exception as e:
                print("Error :", e)
                profile = Profile(user=usr)
                profile.save()
                type = usr.profile.account_type

            profile.phone_number = form["phone_number"]
            profile.address = form["address"]
            profile.birthDate = serializeDate(form["birthDate"])

            for course in ["Maths", "Chimie", "Physique", "Francais"]:
                if course+"_Course" in form.keys():
                    exec("profile." + course + "_course = True")
                else:
                    exec("profile." + course + "_course = False")

            profile.save()

            if type == "Etudiant":
                ModifyStudent(profile, form)
            elif type == "Coach":
                ModifyCoach(profile, form)

            return HttpResponseRedirect("/users/me")

        except Exception as e:
            print("Error :", e)
            return HttpResponseRedirect('/05/')
    else:
        return HttpResponseRedirect('/05/')


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
            print(coaches)

            return render(request, "users/requests.html", locals())
        else:
            return HttpResponseRedirect("/05/")
    else:
        if request.user.is_authenticated():
            if request.user.is_superuser:
                student_requests = studentRequest.objects.all().exclude(
                    is_closed=True)
                student_requests_closed = studentRequest.objects.all().exclude(
                    is_closed=False)

                return render(request, "users/requestsAdmin.html", locals())
            else:
                return HttpResponseRedirect("/05/")
        else:
            return HttpResponseRedirect("/05/")


def thanksCoaches(coaches):
    author = "L'équipe CAD"
    title = "Merci d'avoir répondu présent"
    content = "Merci d'avoir répondu présent à la requête de {} {}. \
    Malheureusement, vous n'avez pas été choisit pour donner cours à \
    cet étudiant. Mais ne vous en faites pas, voitre tour viendra !"
    for coach in coaches:
        new_notif = Notification(
            user=coach.user, author=author, title=title, content=content)
        new_notif.save()


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
    coach.nbStudents += 1

    s_request.save()
    student.save()
    coach.save()

    author = "L'équipe CAD"
    title = "Félicitations !"
    content = "Vous avez été choisit pour enseigner à {} {} ! Vous pouvez \
    vous rendre sur votre profil pour retrouver les coordonées de cet \
    étudiant".format(student.first_name, student.last_name)
    new_Notif = Notification(
        user=coach.user, author=author, title=title, content=content)
    new_Notif.save()

    thanksCoaches(other_coaches)

    return HttpResponse("success")


def requestManage(request):
    if request.method != "POST":
        return HttpResponseRedirect("/05/")

    if request.POST["decision"] == 'true':
        student_request = studentRequest.objects.get(id=request.POST["id"])
        coach = User.objects.get(id=request.POST["coach"])
        student_request.coaches.add(coach.profile)
        student_request.save()
        return HttpResponse("A été ajouté")

    return HttpResponse("N'a pas été ajouté")
