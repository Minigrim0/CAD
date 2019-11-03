from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
import datetime

from users.models import studentRequest, Profile
from default.models import Article, Mail


@staff_member_required
def adminPage(request):
    nbr_accounts = len(User.objects.all())
    nbr_students = len(User.objects.filter(profile__account_type="Etudiant"))
    nbr_coaches = len(User.objects.filter(profile__account_type="Coach"))
    nbr_other = nbr_accounts - nbr_students - nbr_coaches
    nbr_requests = len(studentRequest.objects.all().exclude(is_closed=True))

    return render(request, "admin.html", locals())


@staff_member_required
def mailAdminView(request):
    mails = Mail.objects.all()
    return render(request, 'mailsAdmin.html', locals())


@staff_member_required
def mailAdminModify(request):
    if request.method == "POST":
        form = request.POST
        mail = Mail.objects.get(id=int(form['id']))
        mail.name = form['name'].replace("\r", " ")
        mail.subject = form['subject'].replace("\r", " ")
        mail.content = form['content'].replace("\r", " ")
        mail.save()

    return HttpResponseRedirect("/administration/mails/")


@staff_member_required
def mailAdminCreate(request):
    if request.method == "POST":
        form = request.POST
        mail = Mail()
        mail.name = form['name'].replace("\r", " ")
        mail.subject = form['subject'].replace("\r", " ")
        mail.content = form['content'].replace("\r", " ")
        mail.save()

        return HttpResponseRedirect("/administration/mails/")
    else:
        return render(request, 'mailsAdminCreate.html',)


@staff_member_required
def articleAdminView(request):
    articles = Article.objects.all()
    return render(request, "articlesAdmin.html", locals())


@staff_member_required
def articleAdminModify(request):
    if request.method == "POST":
        form = request.POST
        article = Article.objects.get(id=int(form['id']))
        article.title = form['title'].replace("\r", " ")
        article.subTitle = form['subTitle'].replace("\r", " ")
        article.content = form['Content'].replace("\r", " ")
        article.save()

    return HttpResponseRedirect("/administration/articles/")


@staff_member_required
def userAdminView(request, string=""):
    print(string)
    if string == "":
        users = User.objects.all()
    elif string == "students":
        users = User.objects.filter(profile__account_type="Etudiant")
    elif string == "coaches":
        users = User.objects.filter(profile__account_type="Coach")
    else:
        users = User.objects.all().exclude(profile__account_type="Coach")
        users = users.exclude(profile__account_type="Etudiant")

    firstUser = users[0].username

    level_ = {'5': 'Langue maternelle',
              '4': 'Très bon',
              '3': 'Bon',
              '2': 'Notions de base',
              '1': 'Aucun'}

    lang_ = {'French': 'Francais',
             'Dutch': 'Néerlandais',
             'English': 'Anglais'}

    vars_ = {
        'a_users': users,
        'a_firstUserUsername': firstUser,
        "i_langLevel": level_,
        "i_lang": lang_}

    return render(request, 'userAdmin.html', vars_)


@staff_member_required
def reactivate(request, string=""):
    if string == "":
        return HttpResponseRedirect("/05/")

    usr = User.objects.get(username=string)
    usr.is_active = True
    usr.save()
    return HttpResponseRedirect("/administration")


def serializeDate(date_):
    """
        returns the date from "day month year" to "ddmmyyyy"
    """
    months = [
        "janvier",
        "février",
        "mars",
        "avril",
        "mai",
        "juin",
        "juillet",
        "aout",
        "septembre",
        "octobre",
        "novembre",
        "décembre"]
    date_ = date_.split()
    date_str = date_[0]
    if len(str(date_[0])) == 1:
        date_str = "0" + date_str

    if len(str(months.index(date_[1])+1)) == 1:
        date_str += "0" + str(months.index(date_[1])+1)
    else:
        date_str += str(months.index(date_[1])+1)

    date_str += str(date_[2])

    return datetime.datetime.strptime(date_str, "%d%m%Y")


def modifyDays(profile, form):
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


def modifyStudent(profile, form):

    sa = profile.studentaccount
    sa.NeedsVisit = False
    if form["Visit"] != "NoVisit":
        sa.NeedsVisit = True

    sa.comments = form["comments"]

    sa.tutor_firstName = form["tutorFirstName"]
    sa.tutor_name = form["tutorLastName"]

    if "confirmedAccount" in form.keys():
        sa.confirmedAccount = True
    else:
        sa.confirmedAccount = False
    sa.save()


def modifyCoach(profile, form):
    ca = profile.coachaccount

    ca.school = form["school"]
    ca.IBAN = form["IBAN"]
    ca.nationalRegisterID = form["natRegID"]

    ca.French_level = form["Frenchlevel"]
    ca.English_level = form["Englishlevel"]
    ca.Dutch_level = form["Dutchlevel"]

    ca.confirmedAccount = form["status"]
    ca.save()


@staff_member_required
def modifyUser(request):
    # Check if the way the user accessed this url is correct
    if request.method != "POST":
        return HttpResponseRedirect('/administration/users/')

    try:
        form = request.POST
        # If the admin wants to 'delete' the user
        if "delete" in form.keys():
            usr = User.objects.get(username=form["username"])
            # First step, deactivate the user's account
            if usr.is_active:
                usr.is_active = False
                usr.save()
            # If already deactivated : delete
            else:
                print("user deleted")
                usr.delete()

            return HttpResponseRedirect("/administration/users/")

        # If the admin wants to re-activate the user's account
        elif "reactivate" in form.keys():
            return HttpResponseRedirect(
                "/administration/reactivate/"+form["username"])

        # Else, the admin wants to modify the user
        usr = User.objects.get(username=form["username"])
        usr.first_name = form["firstName"]
        usr.last_name = form["lastName"]
        usr.email = form["mail"]
        usr.save()  # Saves basic user model
        profile = usr.profile

        try:  # Checks if the user as a profile extension
            type = profile.account_type  # Get account type to try
        except Exception as e:
            print("Error :", e)
            profile = Profile(user=usr)
            profile.save()
            type = usr.profile.account_type

        # Modifications that apply for all type of account
        profile.phone_number = form["phone_number"]
        profile.address = form["address"]
        profile.birthDate = serializeDate(form["birthDate"])

        if "verifiedAccount" in form.keys():
            profile.verifiedAccount = True
        else:
            profile.verifiedAccount = False

        for course in ["Maths", "Chimie", "Physique", "Francais"]:
            if course+"_Course" in form.keys():
                exec("profile." + course + "_course = True")
            else:
                exec("profile." + course + "_course = False")
        profile.save()

        # Modifications that only apply to student type account
        if type == "Etudiant":
            modifyStudent(profile, form)
        # Modifications that only apply to coach type account
        elif type == "Coach":
            modifyCoach(profile, form)

        # Redirect to administration
        return HttpResponseRedirect("/administration/users/")

    except Exception as e:  # In case an error occurs
        print("Error :", e)  # Print it
        return HttpResponseRedirect('/administration/users')
