from dal import autocomplete

from django.contrib.auth.models import User
from django.db.models import QuerySet


class CoachAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self) -> QuerySet:
        """Returns a queryset with results filtered from the query"""
        qs = User.objects.filter(profile__account_type="b")

        if self.q:
            qs = qs.filter(first_name__istartswith=self.q)

        return qs
