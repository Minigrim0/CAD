from django import template
from django.contrib.auth.models import User
from users.models import StudentRequest, Notification, CoachAccount

register = template.Library()


@register.simple_tag
def coach_schedule(coach: User, request: StudentRequest):
    return coach.profile.coachaccount.schedule(request)


@register.simple_tag
def accepted_by_coach(request: StudentRequest, coach: CoachAccount):
    return request.coachrequestthrough_set.get(coach=coach).has_accepted


@register.simple_tag
def final_schedule(coach: CoachAccount, student: User):
    request = coach.studentrequest_set.get(student=student)
    return request.finalschedule


@register.simple_tag
def read_notification(notification: Notification):
    notification.read = True
    notification.save()


@register.simple_tag
def nb_notifs(user: User):
    return user.notification_set.filter(read=False).count()
