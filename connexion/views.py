import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def connexion(request):
    """ Connexion view

    Args:
        request (request): The request object needed by all views

    Returns:
        HttpResponseRedirect: a redirection to the home page in case of unsuccessfull login
        render : A render of the page in case the login was successfull
    """
    if request.method != "POST":
        view_title = "Connexion"
        return render(request, 'connexion.html', locals())

    form = request.POST
    email = form["coMail"]
    password = form["coPass"]

    try:
        user = User.objects.get(email=email)  # Get user obj via its email
        if user is None:
            raise Exception

        authuser = authenticate(username=user.username, password=password)
        if authuser:
            login(request, authuser)
            messages.add_message(
                request, messages.SUCCESS,
                "Rebonjour {}".format(request.user.first_name))
        else:
            messages.add_message(
                request, messages.ERROR,
                "Vos identifiants ne correspondent à \
                aucun compte!")
    except Exception as e:
        logging.warning("Error while connecting user : {}".format(e))

        messages.add_message(
            request, messages.ERROR,
            "Vos identifiants ne correspondent à \
            aucun compte!")

    next = request.GET.get("next", "")
    if next != "":
        return HttpResponseRedirect(next)
    return HttpResponseRedirect(reverse("home"))
