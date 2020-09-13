from django import template

register = template.Library()


@register.simple_tag
def coach_schedule(coach, request):
    return coach.profile.coachaccount.schedule(request)


@register.simple_tag
def accepted_by_coach(request, coach):
    return request.coachrequestthrough_set.get(
        coach=coach).has_accepted
