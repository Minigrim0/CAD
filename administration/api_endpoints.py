from datetime import datetime

from default.models import Mail
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from inscription.utils import getUser
from users.models import FollowElement, Transaction, StudentRequest

import administration.utils as utils


@staff_member_required
@require_http_methods(["POST"])
def create_new_request(request) -> JsonResponse:
    """Generates a new studentRequest if the student has no pending request

    Returns:
        JsonResponse: A Json response containing information about whether the request succeeded or not,
        and information aout the failure if necessary
    """
    student = get_object_or_404(User, username=request.POST.get("user", None))
    if StudentRequest.objects.filter(student=student, is_closed=False).count():
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
def set_new_coach(request) -> JsonResponse:
    """Force a new coach for a student. The endpoint creates a finished request in order to make things work properly

    Returns:
        JsonResponse: A Json Response containing information about the coach
    """
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

    StudentRequest.objects.create(
        student=student,
        is_closed=True,
        choosenCoach=coach_account,
        finalschedule=finalSchedule,
    )

    return JsonResponse({"coach_name": f"{coach.first_name} {coach.last_name}"})


@staff_member_required
@require_http_methods(["POST"])
def chooseCoach(request) -> HttpResponse:
    """Selects the given coach from the studentRequest as the one chosen by the administration

    Returns:
        HttpResponse: A response containing the text "success" if no error occured (Otherwise an Http500)
    """
    query = request.POST

    studentrequest = StudentRequest.objects.get(id=query["id"])

    # Profile objects
    coach = studentrequest.coaches.get(pk=query["coach"])
    other_coaches = studentrequest.coaches.all().exclude(pk=query["coach"])
    finalschedule = query["schedule"]

    studentrequest.is_closed = True
    studentrequest.choosenCoach = coach
    studentrequest.finalschedule = finalschedule
    studentrequest.save()

    student = studentrequest.student.profile.studentaccount
    student.coach = coach
    student.save()

    utils.advert_actors(student, coach, finalschedule)

    utils.thanksCoaches(other_coaches, student)

    return HttpResponse("success")


@staff_member_required
@require_http_methods(["POST"])
def modify_balance(request) -> JsonResponse:
    """Creates a transaction from or to the student's account, updating its balance

    Returns:
        JsonResponse: A JsonResponse containing the new balance of the student
    """
    student = User.objects.get(username=request.POST["user"])
    isCoachLaunching = StudentRequest.objects.filter(student=student).count() == 0

    tran = Transaction(student=student.profile.studentaccount)
    tran.amount = request.POST["amout_add"]
    tran.admin = User.objects.get(username=request.POST["approver"])
    tran.comment = "{} du solde via l'administration".format(
        "augmetation" if int(request.POST["amout_add"]) > 0 else "diminution"
    )
    tran.save()

    if isCoachLaunching:
        studentAccount = student.profile.studentaccount
        studentAccount.confirmedAccount = True
        studentAccount.save()

        utils.create_studentRequest(student)

    new_balance = float(student.profile.studentaccount.balance)
    if new_balance < 0 and float(tran.amount) < 0:
        mail = Mail.objects.get(role="d")
        mail.send(student, bcc=["cadcours@cadcoursadomicile.com"])

    return JsonResponse({"new_balance": new_balance})


@staff_member_required
@require_http_methods(["POST"])
def sendUnsubscriptionMail(request) -> HttpResponse:
    """Sends an email proposing a user to unsubscribe from the website (If the account is not confirmed)

    Returns:
        HttpResponse: A response indicating success if nothing went wrong
    """
    user = getUser(request.POST.get("user_key"))
    mail = Mail.objects.get(role="c")
    mail.send(user)

    student_account = user.profile.studentaccount
    student_account.unsub_proposal = True
    student_account.save()
    return HttpResponse("Success")


@staff_member_required
def activate(request) -> HttpResponse:
    """Either activate a deactivated user of deactivate an active user

    Returns:
        HttpResponse: A response indicating success if nothing went wrong
    """
    userid = request.GET.get("userid", -1)
    active = request.GET.get("active", "false") == "true"
    usr = get_object_or_404(User, id=userid)

    usr.is_active = active
    usr.save()
    return HttpResponse("Success")


@staff_member_required
@require_http_methods(["POST"])
def approve_course(request) -> HttpResponse:
    """Marks a course as approved by the administration or deletes it

    Returns:
        HttpResponse: A response indicating success if nothing went wrong
    """
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
@require_http_methods(["GET"])
def request_informations(request) -> JsonResponse:
    """Returns information about a student request, to put it in the closed student requests"""
    id = request.GET.get("id", None)
    student_request = get_object_or_404(StudentRequest, id=id)
    rendered = render(
        request, "student_request_section.html", {"student_request": student_request}
    )

    return JsonResponse(
        {
            "content": rendered.content.decode("utf-8"),
        }
    )
