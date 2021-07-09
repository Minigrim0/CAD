from django import template
from django.contrib.auth.models import User
from users.models import StudentRequest, Notification, CoachAccount

register = template.Library()


@register.simple_tag
def coach_schedule(coach: User, request: StudentRequest) -> str:
    """Shows the schedule of a coach for a given sudent request"""
    return coach.profile.coachaccount.schedule(request)


@register.simple_tag
def accepted_by_coach(request: StudentRequest, coach: CoachAccount) -> bool:
    """Returns a boolean indicating whether the coach has accepted the request or not"""
    return request.coachrequestthrough_set.get(coach=coach).has_accepted


@register.simple_tag
def final_schedule(coach: CoachAccount, student: User) -> str:
    """Shows the final schedule of a request"""
    request = coach.studentrequest_set.filter(student=student).last()
    return request.finalschedule


@register.simple_tag
def read_notification(notification: Notification):
    """Marks a notification as read"""
    notification.read = True
    notification.save()


@register.simple_tag
def nb_notifs(user: User) -> int:
    """Shows the amount of unread notifications a user has"""
    return user.notification_set.filter(read=False).count()
