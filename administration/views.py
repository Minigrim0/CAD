from datetime import datetime, timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from djqscsv import render_to_csv_response

from administration.forms import (
    ArticleForm,
    MailForm,
    StudentAdminForm,
    CoachAdminForm,
    OtherAdminForm,
    newCoachForm,
)
from administration.utils import modifyUser, populate_data
from default.models import Article, Mail, Message
from users.models import FollowElement, StudentRequest, Transaction


@staff_member_required
def adminPage(request) -> HttpResponse:
    """The home view of the administration of the website

    Args:
        request (request): request object needed by all the views

    Returns:
        HttpResponse: The render of the administration home page
    """
    nbr_accounts = User.objects.all().count()
    nbr_students = User.objects.filter(profile__account_type="a").count()
    nbr_coaches = User.objects.filter(profile__account_type="b").count()
    nbr_other = nbr_accounts - nbr_students - nbr_coaches  # skipcq PYL-W0641
    nbr_requests = StudentRequest.objects.all().exclude(is_closed=True).count()  # skipcq PYL-W0641
    nbr_messages = Message.objects.filter(seen=False).count()  # skipcq PYL-W0641

    view_title = "Administration"  # skipcq PYL-W0641

    return render(request, "admin.html", locals())


@staff_member_required
def mailAdminView(request) -> HttpResponse:
    """Mail modification view in the administration

    Args:
        request (request): request object needed by all the views

    Returns:
        HttpResponse: The render of the mail modification page
    """
    if request.method == "POST":
        form = request.POST
        mail = Mail.objects.get(id=int(form["mailid"]))
        mail.name = form["name"].replace("\r", " ")
        mail.subject = form["subject"].replace("\r", " ")
        mail.content = form["content"].replace("\r", " ")
        mail.role = form["role"]
        mail.save()

    mails = [MailForm(instance=mail) for mail in Mail.objects.all().exclude(role="i")]  # skipcq PYL-W0641
    view_title = "Mails"  # skipcq PYL-W0641

    return render(request, "mailsAdmin.html", locals())


@staff_member_required
def articleAdminView(request) -> HttpResponse:
    """Articles modification view in the administration

    Args:
        request (request): request object needed by all the views

    Returns:
        HttpResponse: The render of the article modification page
    """
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = get_object_or_404(Article, name=form.cleaned_data["name"])
            article.title = form.cleaned_data["title"].replace("\r", " ")
            article.subtitle = form.cleaned_data["subtitle"].replace("\r", " ")
            article.content = form.cleaned_data["content"].replace("\r", " ")
            article.save()

    articles = [ArticleForm(instance=article) for article in Article.objects.all()]  # skipcq PYL-W0641
    view_title = "Articles"  # skipcq PYL-W0641

    return render(request, "articlesAdmin.html", locals())


@staff_member_required
def mailAdminCreate(request) -> HttpResponse:
    """Mail creation view in the administration

    Args:
        request (request): request object needed by all the views

    Returns:
        HttpResponse: The render of the mail creation page
    """
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
    view_title = "Créer un mail"  # skipcq PYL-W0641

    return render(request, "mailsAdminCreate.html", locals())


@staff_member_required
def courses(request) -> HttpResponse:
    """A view rendering all the courses that happened on the website

    Args:
        request (request): request object needed by all the views

    Returns:
        HttpResponse: The render of the course page
    """
    view_title = "Cours donnés"

    sorter = request.GET.get("sort_by", "-date")
    if (
        sorter not in [
            "date", "-date", "approved", "-approved", "student__username",
            "-student__username", "coach__username", "-coach__username"]
    ):
        sorter = "date"

    courses_list = FollowElement.objects.all().order_by(sorter)
    paginator = Paginator(courses_list, 25)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "courses.html",
        {
            'page_obj': page_obj,
            "view_title": view_title,
            "sorter": sorter
        }
    )


@staff_member_required
def transactions(request) -> HttpResponse:
    """A view rendering all the transactions that happened on the website

    Args:
        request (request): request object needed by all the views

    Returns:
        HttpResponse: The render of the transaction view
    """
    transaction_list = Transaction.objects.all().order_by("date")  # skipcq PYL-W0641
    view_title = "Transactions effectuées"  # skipcq PYL-W0641

    return render(request, "transactions.html", locals())


@staff_member_required
def user_list(request) -> HttpResponse:
    """A view rendering users' basic information based on certain queries

    Args:
        request (request): request object needed by all the views

    Returns:
        HttpResponse: The render of the user list page
    """
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

    view_title = "Utilisateurs"  # skipcq PYL-W0641
    return render(request, "user_list.html", locals())


@staff_member_required
def user_admin_view(request) -> HttpResponse:
    """A view rendering every information about a certain user

    Args:
        request (request): request object needed by all the views

    Returns:
        HttpResponse: The render of the user_details page
    """
    username = request.GET.get("user", "")
    usertype = request.GET.get("type", "")

    if username == "":
        return HttpResponseRedirect("{}?type={}".format(reverse("userlist"), usertype))
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

    if request.method == "POST" and form.is_valid():
        modifyUser(username, form)

    view_title = "{} {}".format(user.last_name, user.first_name)
    context.update({"form": form, "form_user": user, "view_title": view_title})
    return render(
        request,
        "user_admin_view.html",
        context,
    )


@staff_member_required
def message_list(request) -> HttpResponse:
    """A view rendering a list of every messages received from the contact form

    Args:
        request (request): request object needed by all the views

    Returns:
        HttpResponse: The render of the message page
    """
    status = request.GET.get("status", "")
    if status == "unread":
        messages = Message.objects.filter(seen=False)  # skipcq PYL-W0641
    elif status == "read":
        messages = Message.objects.filter(seen=True)
    else:
        messages = Message.objects.all()

    view_title = "Messages"  # skipcq PYL-W0641
    return render(request, "message_list.html", locals())


@staff_member_required
def message_admin_view(request) -> HttpResponse:
    """A view rendering every information about a certain message sent from the contact form

    Args:
        request (request): request object needed by all the views

    Returns:
        HttpResponse: The render of the message_details page
    """
    id = request.GET.get("id", -1)
    message = get_object_or_404(Message, id=id)
    message.seen = True
    message.save()

    view_title = "Messages"  # skipcq PYL-W0641
    return render(request, "message_admin_view.html", locals())


@staff_member_required
def student_requests(request) -> HttpResponse:
    """A view rendering informations about every student request

    Args:
        request (request): request object needed by all the views

    Returns:
        HttpResponse: The render of the requests page
    """
    opened_student_requests = (  # skipcq PYL-W0641
        StudentRequest.objects.all().exclude(is_closed=True).order_by("-id")
    )
    closed_student_requests = (  # skipcq PYL-W0641
        StudentRequest.objects.all().exclude(is_closed=False).order_by("-id")
    )

    view_title = "Requêtes"  # skipcq PYL-W0641
    return render(request, "requestsAdmin.html", locals())


@staff_member_required
def download_courses(request):
    from_date = request.GET["from"]
    to_date = request.GET["to"]

    from_date = datetime.strptime(from_date, "%d/%m/%Y")
    to_date = datetime.strptime(to_date, "%d/%m/%Y")

    qs = FollowElement.objects.filter(
        date__gte=from_date, date__lt=to_date, approved=True
    ).values(
        'date', 'startHour', 'endHour',
        'student__first_name', 'student__last_name',
        'coach__first_name', 'coach__last_name',
        'comments')
    return render_to_csv_response(qs)
