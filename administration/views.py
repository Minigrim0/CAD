import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseRedirect)
from django.shortcuts import render
from django.urls import reverse

from administration.forms import ArticleForm, MailForm
from administration.utils import modifyCoach, modifyStudent
from cad.settings import EMAIL_HOST_USER, DEBUG
from default.models import Article, Mail
from inscription.utils import getUser
from users.models import FollowElement, Profile, studentRequest, Transaction


@staff_member_required
def adminPage(request):
    nbr_accounts = len(User.objects.all())
    nbr_students = len(User.objects.filter(profile__account_type="Etudiant"))
    nbr_coaches = len(User.objects.filter(profile__account_type="Coach"))
    nbr_other = nbr_accounts - nbr_students - nbr_coaches
    nbr_requests = len(studentRequest.objects.all().exclude(is_closed=True))

    view_title = "adminisitration"

    return render(request, "admin.html", locals())


@staff_member_required
def mailAdminView(request):
    if request.method == "POST":
        form = request.POST
        mail = Mail.objects.get(id=int(form['mailid']))
        mail.name = form['name'].replace("\r", " ")
        mail.subject = form['subject'].replace("\r", " ")
        mail.content = form['content'].replace("\r", " ")
        mail.role = form['role']
        mail.save()

    mails = [MailForm(instance=mail) for mail in Mail.objects.all()]
    view_title = "mails"

    return render(request, 'mailsAdmin.html', locals())


@staff_member_required
def articleAdminView(request):
    if request.method == "POST":
        form = request.POST
        article = Article.objects.get(id=int(form['articleid']))
        article.title = form['title'].replace("\r", " ")
        article.subtitle = form['subtitle'].replace("\r", " ")
        article.content = form['content'].replace("\r", " ")
        article.save()

    articles = [ArticleForm(instance=article) for article in Article.objects.all()]
    view_title = "articles"

    return render(request, "articlesAdmin.html", locals())


@staff_member_required
def mailAdminCreate(request):
    if request.method == "POST":
        form = request.POST
        mail = Mail()
        mail.name = form['name'].replace("\r", " ")
        mail.subject = form['subject'].replace("\r", " ")
        mail.content = form['content'].replace("\r", " ")
        mail.role = form['role']
        mail.save()

        return HttpResponseRedirect(reverse("mails_admin"))
    else:
        form = MailForm()

        view_name = "créer un mail"

        return render(request, 'mailsAdminCreate.html', locals())


@staff_member_required
def courses(request):
    courses = FollowElement.objects.all().order_by("date")
    view_name = "cours donnés"

    return render(request, "courses.html", locals())


@staff_member_required
def transactions(request):
    transactions = Transaction.objects.all().order_by("date")
    view_name = "transactions effectuées"

    return render(request, "transactions.html", locals())


@staff_member_required
def userAdminView(request):
    usertype = request.GET.get("type", "")
    if usertype == "":
        users = User.objects.all()
    elif usertype == "students":
        users = User.objects.filter(profile__account_type="Etudiant")
    elif usertype == "coaches":
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
        "i_lang": lang_,
        "view_name": "utilisateurs"
    }

    return render(request, 'userAdmin.html', vars_)


@staff_member_required
def reactivate(request, username=""):
    if username == "":
        return HttpResponseRedirect(reverse("Error_view"))

    usr = User.objects.get(username=username)
    usr.is_active = True
    usr.save()
    return HttpResponseRedirect(reverse("home_admin"))


@staff_member_required
def modifyUser(request):
    # Check if the way the user accessed this url is correct
    if request.method != "POST":
        if request.META.get('HTTP_REFERER') is not None:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(reverse("user_admin"))
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
                logging.warning("user {} deleted".format(usr))
                usr.delete()

            return HttpResponseRedirect(reverse("user_admin"))

        # If the admin wants to re-activate the user's account
        elif "reactivate" in form.keys():
            return HttpResponseRedirect(
                reverse("reactivate_user", kwargs={'string': form["username"]}))

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
            logging.warning("Error when getting the user's profile : {}".format(e))
            profile = Profile(user=usr)
            profile.save()
            type = usr.profile.account_type

        # Modifications that apply for all type of account
        profile.phone_number = form["phone_number"]
        profile.address = form["address"]
        profile.birthDate = form["birthDate"]

        if "verifiedAccount" in form.keys():
            profile.verifiedAccount = True
        else:
            profile.verifiedAccount = False

        for course in ["Maths", "Chimie", "Physique", "Francais"]:
            if "{}_Course".format(course) in form.keys():
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
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:  # In case an error occurs
        logging.critical("Error while modifying user : {}".format(e))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def sendUnsubscriptionMail(request):
    if request.method != "POST":
        return HttpResponseBadRequest(
            "Invalid method : Requets must be type POST")

    user = getUser(request.POST.get("user_key"))
    mail = Mail.objects.get(role='c')
    if not DEBUG:
        send_mail(
            mail.clean_header, mail.formatted_content(user), EMAIL_HOST_USER,
            [user.email])
    else:
        messages.warning(request, "L'envoi d'email est désactivé sur cette platforme!")

    student_account = user.profile.studentaccount
    student_account.unsub_proposal = True
    student_account.save()
    return HttpResponse("Success")
