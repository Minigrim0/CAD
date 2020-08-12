from dal import autocomplete

from django.contrib.auth.models import User


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = User.objects.filter(profile__account_type="b")

        if self.q:
            qs = qs.filter(first_name__istartswith=self.q)

        return qs
