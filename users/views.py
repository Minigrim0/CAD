from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from administration.views import serializeDate
from users.models import Notification, studentRequest


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


def modifyUser(request):
    if request.method == "POST":
        try:
            form = request.POST
            if "modify" in form.keys():
                usr = User.objects.get(username=form["username"])
                usr.first_name = form["firstName"]
                usr.last_name = form["lastName"]
                usr.email = form["mail"]
                usr.save()
                profile = usr.profile()

                try:
                    type = usr.profile.account_type

                    profile.phone_number = form["phone_number"]
                    profile.address = form["address"]
                    profile.birthDate = serializeDate(form["birthDate"])

                    for course in ["Maths", "Chimie", "Physique", "Francais"]:
                        if course+"_Course" in form.keys():
                            exec("usr.profile." + course + "_course = True")
                        else:
                            exec("usr.profile." + course + "_course = False")

                    if type == "Etudiant":
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
                                    profile.wanted_schedule += form[
                                        day+"Start"] + "/"
                                    profile.wanted_schedule += form[
                                        day+"End"] + "."
                            except KeyError:
                                profile.wanted_schedule += "0/0/0."

                        profile.NeedsVisit = False
                        if form["Visit"] != "NoVisit":
                            profile.NeedsVisit = True

                        profile.comments = form["comments"]

                        profile.tutor_firstName = form["tutorFirstName"]
                        profile.tutor_name = form["tutorName"]
                    elif type == "Coach":
                        profile.school = form["school"]
                        profile.IBAN = form["IBAN"]
                        profile.nationalRegisterID = form["natRegID"]

                        profile.French_level = form["Frenchlevel"]
                        profile.English_level = form["Englishlevel"]
                        profile.Dutch_level = form["Dutchlevel"]

                    profile.save()

                except Exception as e:
                    print("Error :", e)

                return HttpResponseRedirect("/users/me")
            else:
                usr = User.objects.get(username=form["username"])
                usr.is_active = False
                usr.save()
                logout(request)
                return HttpResponseRedirect("/12/")

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
                student_requests = studentRequest.objects.all()

                return render(request, "users/requestsAdmin.html", locals())
            else:
                return HttpResponseRedirect("/05/")
        else:
            return HttpResponseRedirect("/05/")


def chooseCoach(request):
    if request.method != "POST":
        print("went through here")
        return HttpResponse("/05/")

    print("went through here")
    return HttpResponse(
        "Yay-{}-{}".format(request.POST['coach'], request.POST['id']))


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
