import logging

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse

from users.models import Notification, StudentRequest
from users.views import ErrorView


def get_users(request) -> JsonResponse:
    """Returns the users linked to the email provided

    Returns:
        JsonResponse: a dictionnary containing the name of the users with the given email address
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method : Request type must be 'POST'")

    email = request.POST.get("email", "")
    users = User.objects.filter(email=email)

    userData = []
    for user in users:
        userData.append(
            ("{} {}".format(user.first_name, user.last_name), user.username)
        )

    return JsonResponse({"users": userData})


@login_required
def send_notif(request) -> HttpResponse:
    """Sends a notification to the concerned user

    Returns:
        HttpResponse: A small message indicating the status of the request
    """
    if request.method == "POST":
        user = User.objects.get(username=request.POST["user"])
        notif = Notification()
        notif.user = user
        notif.title = request.POST["title"]
        notif.content = request.POST["content"]
        notif.author = request.POST["sender"]
        notif.save()
        notif.send_as_mail()

        logging.debug(
            "Added notification (id {}) to {}".format(notif.pk, request.POST["user"])
        )

        return HttpResponse("Success")

    return HttpResponse("failed")


@login_required
def remove_notif(request) -> HttpResponse:
    """Removes a notification

    Raises:
        Http404: In case the notification doesn't exist

    Returns:
        HttpResponse: A message indicating the request went well
    """
    if request.method != "POST":
        return ErrorView(request)

    user = request.user
    notification = get_object_or_404(Notification, id=request.POST["id"])
    if notification.user.username != user.username:
        raise Http404()
    notification.delete()

    return HttpResponse("success")


@login_required
def acceptRequest(request) -> HttpResponse:
    """Accepts the request given as post parameter

    Returns:
        HttpResponse: A message indicating the request went well
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method : Request must type be 'POST'")

    accepted = request.POST.get("decision", False) == "true"
    coachschedule = request.POST.get("schedule", "")

    student_request = get_object_or_404(StudentRequest, id=request.POST["id"])
    coach = get_object_or_404(User, id=request.POST["coach"])
    student_request.coaches.add(coach.profile.coachaccount)
    student_request.save()

    throughmodel = student_request.coachrequestthrough_set.get(
        coach=coach.profile.coachaccount
    )
    throughmodel.has_accepted = accepted
    throughmodel.coachschedule = coachschedule
    throughmodel.save()

    return HttpResponse("Success")
