import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404

from administration.forms import ArticleForm, MailForm, StudentAdminForm, CoachAdminForm, OtherAdminForm
from administration.utils import modifyUser, populate_data
from cad.settings import DEBUG
from default.models import Article, Mail, Message
from inscription.utils import getUser
from users.models import FollowElement, studentRequest, Transaction


@staff_member_required
def adminPage(request):
    nbr_accounts = User.objects.all().count()
    nbr_students = User.objects.filter(profile__account_type="a").count()
    nbr_coaches = User.objects.filter(profile__account_type="b").count()
    nbr_other = nbr_accounts - nbr_students - nbr_coaches
    nbr_requests = studentRequest.objects.all().exclude(is_closed=True).count()
    nbr_messages = Message.objects.filter(seen=False).count()

    view_title = "Administration"

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

    mails = [MailForm(instance=mail) for mail in Mail.objects.all().exclude(role="i")]
    view_title = "Mails"

    return render(request, 'mailsAdmin.html', locals())


@staff_member_required
def articleAdminView(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = get_object_or_404(Article, name=form.cleaned_data['name'])
            article.title = form.cleaned_data['title'].replace("\r", " ")
            article.subtitle = form.cleaned_data['subtitle'].replace("\r", " ")
            article.content = form.cleaned_data['content'].replace("\r", " ")
            article.save()

    articles = [ArticleForm(instance=article) for article in Article.objects.all()]
    view_title = "Articles"

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

    form = MailForm()
    view_title = "Créer un mail"

    return render(request, 'mailsAdminCreate.html', locals())


@staff_member_required
def courses(request):
    courses = FollowElement.objects.all().order_by("date")
    view_title = "Cours donnés"

    return render(request, "courses.html", locals())


@staff_member_required
def transactions(request):
    transactions = Transaction.objects.all().order_by("date")
    view_title = "Transactions effectuées"

    return render(request, "transactions.html", locals())


@staff_member_required
def activate(request):
    userid = request.GET.get("userid", -1)
    active = True if request.GET.get("active", "false") == "true" else False
    usr = get_object_or_404(User, id=userid)

    usr.is_active = active
    usr.save()
    return HttpResponse("Success")


@staff_member_required
def user_list(request):
    usertype = request.GET.get("type", "")
    query = request.GET.get("q", "")

    if usertype == "a":
        users = User.objects.filter(profile__account_type="a").order_by('id')
    elif usertype == "b":
        users = User.objects.filter(profile__account_type="b").order_by('id')
    elif usertype == "c":
        users = User.objects.all().exclude(profile__account_type="a").exclude(profile__account_type="b").order_by('id')
    else:
        users = User.objects.all().order_by('id')

    if query != "":
        users = users.filter(username__icontains=query)

    view_title = "Utilisateurs"
    return render(request, "user_list.html", locals())


@staff_member_required
def user_admin_view(request):
    username = request.GET.get("user", "")
    usertype = request.GET.get("type", "")

    if username == "":
        return HttpResponseRedirect("{}?type={}".format(reverse("userlist"), usertype))
    else:
        user = get_object_or_404(User, username=username)

    if request.method == "POST":
        data = request.POST
    else:
        data = populate_data(usertype.lower(), user)

    if usertype.lower() == "a":
        form = StudentAdminForm(data)
    elif usertype.lower() == "b":
        form = CoachAdminForm(data)
    else:
        form = OtherAdminForm(data)

    if request.method == "POST":
        if form.is_valid():
            modifyUser(username, form)

    view_title = "{} {}".format(user.last_name, user.first_name)
    return render(request, "user_admin_view.html", {"form": form, "form_user": user, "view_title": view_title})


@staff_member_required
def sendUnsubscriptionMail(request):
    if request.method != "POST":
        return HttpResponseBadRequest(
            "Invalid method : Requets must be type POST")

    user = getUser(request.POST.get("user_key"))
    mail = Mail.objects.get(role='c')
    if not DEBUG:
        mail.send(user, request.META["HTTP_HOST"])
    else:
        messages.warning(request, "L'envoi d'email est désactivé sur cette platforme!")

    student_account = user.profile.studentaccount
    student_account.unsub_proposal = True
    student_account.save()
    return HttpResponse("Success")


@staff_member_required
def message_list(request):
    status = request.GET.get("status", "")
    if status == "unread":
        messages = Message.objects.filter(seen=False)
    elif status == "read":
        messages = Message.objects.filter(seen=True)
    else:
        messages = Message.objects.all()

    view_title = "Messages"
    return render(request, 'message_list.html', locals())


@staff_member_required
def message_admin_view(request):
    id = request.GET.get("id", -1)
    message = get_object_or_404(Message, id=id)
    message.seen = True
    message.save()

    view_title = "Messages"
    return render(request, 'message_admin_view.html', locals())
