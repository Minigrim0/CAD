from datetime import datetime

from default.models import Mail
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from inscription.utils import getUser
from users.models import FollowElement, Notification, Transaction, studentRequest

import administration.utils as utils


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
        utils.create_studentRequest(student)
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

    utils.thanksCoaches(other_coaches, student)

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
        studentAccount = student.profile.studentaccount
        studentAccount.confirmedAccount = True
        studentAccount.save()

        utils.create_studentRequest(student)

    return JsonResponse({"new_balance": student.profile.studentaccount.balance})


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
def activate(request):
    userid = request.GET.get("userid", -1)
    active = True if request.GET.get("active", "false") == "true" else False
    usr = get_object_or_404(User, id=userid)

    usr.is_active = active
    usr.save()
    return HttpResponse("Success")


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
