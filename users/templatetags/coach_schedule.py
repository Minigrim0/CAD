from django import template

register = template.Library()


@register.simple_tag
def coach_schedule(coach, request):
    return coach.profile.coachaccount.schedule(request)
