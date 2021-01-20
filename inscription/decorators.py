from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse


def mustnt_be_logged_in(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.user.is_authenticated:
            messages.warning(request, f"Vous êtes connecté en tant que {request.user.first_name} {request.user.last_name}, si vous souhaiter vous inscrire avec un autre compte, déconnectez-vous d'abord")
            return HttpResponseRedirect(reverse("home"))
        return func(*args, **kwargs)
    return wrapper