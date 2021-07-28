from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag
def relation_score(coach: User, student: User) -> int:
    """Shows the score of the relation between a coach and a student"""
    return coach.profile.relationScore(student.profile)
