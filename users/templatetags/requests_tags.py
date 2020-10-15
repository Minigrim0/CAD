from django import template
from users.models import studentRequest

register = template.Library()


@register.simple_tag
def coach_schedule(coach, request):
    return coach.profile.coachaccount.schedule(request)


@register.simple_tag
def accepted_by_coach(request, coach):
    return request.coachrequestthrough_set.get(
        coach=coach).has_accepted


@register.simple_tag
def final_schedule(coach, student):
    request = coach.studentrequest_set.get(student=student)
    return request.finalschedule
