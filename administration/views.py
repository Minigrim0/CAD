from datetime import datetime

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
    HttpResponseBadRequest,
)
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404

from administration.forms import (
    ArticleForm,
    MailForm,
    StudentAdminForm,
    CoachAdminForm,
    OtherAdminForm,
    newCoachForm,
)
from administration.utils import (
    modifyUser,
    populate_data,
    thanksCoaches,
    sendNotifToCoaches,
)
from cad.settings import DEBUG
from default.models import Article, Mail, Message
from inscription.utils import getUser
from users.models import FollowElement, studentRequest, Transaction, Notification


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
        mail = Mail.objects.get(id=int(form["mailid"]))
        mail.name = form["name"].replace("\r", " ")
        mail.subject = form["subject"].replace("\r", " ")
        mail.content = form["content"].replace("\r", " ")
        mail.role = form["role"]
        mail.save()

    mails = [MailForm(instance=mail) for mail in Mail.objects.all().exclude(role="i")]
    view_title = "Mails"

    return render(request, "mailsAdmin.html", locals())


@staff_member_required
def articleAdminView(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = get_object_or_404(Article, name=form.cleaned_data["name"])
            article.title = form.cleaned_data["title"].replace("\r", " ")
            article.subtitle = form.cleaned_data["subtitle"].replace("\r", " ")
            article.content = form.cleaned_data["content"].replace("\r", " ")
            article.save()

    articles = [ArticleForm(instance=article) for article in Article.objects.all()]
    view_title = "Articles"

    return render(request, "articlesAdmin.html", locals())


@staff_member_required
def mailAdminCreate(request):
    if request.method == "POST":
        form = request.POST
        mail = Mail()
        mail.name = form["name"].replace("\r", " ")
        mail.subject = form["subject"].replace("\r", " ")
        mail.content = form["content"].replace("\r", " ")
        mail.role = form["role"]
        mail.save()

        return HttpResponseRedirect(reverse("mails_admin"))

    form = MailForm()
    view_title = "Créer un mail"

    return render(request, "mailsAdminCreate.html", locals())


@staff_member_required
def courses(request):
    courses = FollowElement.objects.all().order_by("date")
    view_title = "Cours donnés"

    return render(request, "courses.html", locals())


@staff_member_required
@require_http_methods(["POST"])
def approve_course(request):
    form = request.POST
    pk = request.POST.get("pk", -1)
    course = get_object_or_404(FollowElement, pk=pk)
    if form["isApproved"] == "true":
        course.approved = True
        Transaction.objects.create(
            student=course.student.profile.studentaccount,
            amount=-course.duration,
            date=datetime.today(),
            admin=request.user,
            comment="paiement pour cours",
        )
        course.save()
    else:
        course.delete()

    return HttpResponse("Success")


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
    usertype = request.GET.get("type", "d")
    query = request.GET.get("q", "")

    if usertype == "a":
        users = User.objects.filter(profile__account_type="a").order_by("id")
    elif usertype == "b":
        users = User.objects.filter(profile__account_type="b").order_by("id")
    elif usertype == "c":
        users = (
            User.objects.all()
            .exclude(profile__account_type="a")
            .exclude(profile__account_type="b")
            .order_by("id")
        )
    else:
        users = User.objects.all().order_by("last_name")

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

    context = {}
    if usertype.lower() == "a":
        form = StudentAdminForm(data)
        context["new_coach_form"] = newCoachForm()
    elif usertype.lower() == "b":
        form = CoachAdminForm(data)
    else:
        form = OtherAdminForm(data)

    if request.method == "POST":
        if form.is_valid():
            modifyUser(username, form)

    view_title = "{} {}".format(user.last_name, user.first_name)
    context.update({"form": form, "form_user": user, "view_title": view_title})
    return render(
        request,
        "user_admin_view.html",
        context,
    )


@staff_member_required
@require_http_methods(["POST"])
def sendUnsubscriptionMail(request):
    user = getUser(request.POST.get("user_key"))
    mail = Mail.objects.get(role="c")
    if not DEBUG:
        mail.send(user)
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
    return render(request, "message_list.html", locals())


@staff_member_required
def message_admin_view(request):
    id = request.GET.get("id", -1)
    message = get_object_or_404(Message, id=id)
    message.seen = True
    message.save()

    view_title = "Messages"
    return render(request, "message_admin_view.html", locals())


@staff_member_required
def student_requests(request):
    student_requests = (
        studentRequest.objects.all().exclude(is_closed=True).order_by("-id")
    )
    student_requests_closed = (
        studentRequest.objects.all().exclude(is_closed=False).order_by("-id")
    )

    view_title = "Requêtes"
    return render(request, "requestsAdmin.html", locals())


@staff_member_required
@require_http_methods(["POST"])
def create_new_request(request):
    """
    from user_admin_view
        Creates a new coach request if the user has no pending request
    """

    student = get_object_or_404(User, username=request.POST.get("user", None))
    if studentRequest.objects.filter(student=student, is_closed=False).count():
        response = {
            "accepted": False,
            "reason": "Une requete ouverte pour cet etudiant existe deja",
        }
    else:
        request = studentRequest.objects.create(student=student)
        sendNotifToCoaches(student.profile, request)
        response = {
            "accepted": True,
        }
    return JsonResponse(response)


@staff_member_required
@require_http_methods(["POST"])
def set_new_coach(request):
    coach_id = request.POST.get("coach", None)
    finalSchedule = request.POST.get("finalSchedule", None)

    student_username = request.POST.get("student", None)
    if coach_id is None:
        return HttpResponseBadRequest("no coach id given")

    coach = get_object_or_404(User, profile__account_type="b", id=coach_id)
    student = get_object_or_404(
        User, username=student_username, profile__account_type="a"
    )

    coach_account = coach.profile.coachaccount
    student_account = student.profile.studentaccount

    student_account.coach = coach_account
    student_account.save()

    studentRequest.objects.create(
        student=student,
        is_closed=True,
        choosenCoach=coach_account,
        finalschedule=finalSchedule,
    )

    return JsonResponse({"coach_name": f"{coach.first_name} {coach.last_name}"})


@staff_member_required
@require_http_methods(["POST"])
def chooseCoach(request):
    """
    Selects a coach to be chosen for a certain request
    """
    query = request.POST

    studentrequest = studentRequest.objects.get(id=query["id"])

    # Profile objects
    coach = studentrequest.coaches.get(pk=query["coach"])
    other_coaches = studentrequest.coaches.all().exclude(pk=query["coach"])
    finalschedule = query["schedule"]
    student = studentrequest.student.profile.studentaccount

    studentrequest.is_closed = True
    studentrequest.choosenCoach = coach
    studentrequest.finalschedule = finalschedule
    student.coach = coach

    studentrequest.save()
    student.save()

    author = "L'équipe CAD"
    title = "Félicitations!"
    content = "Vous avez été choisi pour enseigner à {} {}! Vous pouvez \
    vous rendre sur votre profil pour retrouver les coordonées de cet \
    étudiant".format(
        student.profile.user.first_name, student.profile.user.last_name
    )
    new_Notif = Notification(
        user=coach.profile.user, author=author, title=title, content=content
    )
    new_Notif.send_as_mail()
    new_Notif.save()

    thanksCoaches(other_coaches, student)

    return HttpResponse("success")


@staff_member_required
@require_http_methods(["POST"])
def modify_balance(request):
    isCoachLaunching = (
        True if request.POST.get("isFirstPayment", False) == "true" else False
    )

    student = User.objects.get(username=request.POST["user"])

    tran = Transaction(student=student.profile.studentaccount)
    tran.amount = request.POST["amout_add"]
    tran.admin = User.objects.get(username=request.POST["approver"])
    tran.save()

    if isCoachLaunching:
        newRequest = studentRequest(student=student)
        newRequest.save()

        studentAccount = student.profile.studentaccount
        studentAccount.confirmedAccount = True
        studentAccount.save()

        sendNotifToCoaches(student.profile, newRequest)

    return JsonResponse({"new_balance": student.profile.studentaccount.balance})
