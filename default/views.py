# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from default.forms import contactForm
from default.models import Article, Message


def home(request) -> HttpResponse:
    """Home view

    Returns:
        HttpResponse: A render of the home page
    """
    context = {
        "a_home": Article.objects.filter(name="Accueil")[0],
        "a_info": Article.objects.filter(name="Info")[0],
        "a_video": Article.objects.filter(name="Video")[0],
        "a_coaches": Article.objects.filter(name="Coaches")[0],
        "a_about": Article.objects.filter(name="About")[0],
        "a_contact": Article.objects.filter(name="Contact")[0],
        "view_title": "cours à domicile",
    }

    return render(request, "index.html", context)


def contactView(request) -> HttpResponse:
    """Contact view

    Returns:
        HttpResponseRedirect: A redirection to the home page if the user clicked on "send" in the form
        render: A render of the contact form
    """
    if request.method == "POST":
        form = contactForm(request.POST)
        if form.is_valid():
            msg = Message()
            msg.subject = form.cleaned_data["sujet"]
            msg.content = form.cleaned_data["message"]
            msg.contact_mail = form.cleaned_data["envoyeur"]
            msg.save()
            msg.send_as_mail()

            messages.add_message(
                request, messages.SUCCESS, "Votre message a bien été envoyé!"
            )

            return HttpResponseRedirect(reverse("home"))
    else:
        form = contactForm()

    view_title = "Formulaire de contact"
    return render(request, "contact.html", locals())


def soon(request) -> HttpResponse:
    """Shows the coming soon page

    Returns:
        HttpResponse: A render of the soon page
    """
    return render(request, "soon.html")
