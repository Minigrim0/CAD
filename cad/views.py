from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render

from django.urls import reverse


def chooseLocation(request):
    return render(request, "chooseLocation.html")


def password_reset_done(request):
    messages.success(
        request,
        "Votre mot de passe a bien été réinitialisé, vous pouvez vous connecter avec votre nouveau mot de passe",
    )

    return HttpResponseRedirect(reverse("home"))
