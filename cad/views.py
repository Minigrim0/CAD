from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.shortcuts import render

from django.urls import reverse


def chooseLocation(request) -> HttpResponse:
    """Asks the user which site he wants to visit

    Returns:
        HttpResponse: The rendered page
    """
    return render(request, "chooseLocation.html")


def password_reset_done(request) -> HttpResponseRedirect:
    """Adds a success message for the user

    Returns:
        HttpResponseRedirect: A redirection to the home page
    """
    messages.success(
        request,
        "Votre mot de passe a bien été réinitialisé, vous pouvez vous connecter avec votre nouveau mot de passe",
    )

    return HttpResponseRedirect(reverse("home"))
