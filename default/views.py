# -*- coding: utf-8 -*-
import django
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from default.forms import contactForm
from default.models import Article, Message

from cad.settings import DEBUG


def home(request):
    """Home view

    Args:
        request (request): request object needed by all the views

    Returns:
        render: A render of the home page
    """
    home = Article.objects.filter(name="Accueil")
    info = Article.objects.filter(name="Info")
    video = Article.objects.filter(name="Video")
    coaches = Article.objects.filter(name="Coaches")
    about = Article.objects.filter(name="About")
    contact = Article.objects.filter(name="Contact")

    dico = {
        'a_home': home[0],
        'a_info': info[0],
        'a_video': video[0],
        'a_coaches': coaches[0],
        'a_about': about[0],
        'a_contact': contact[0],
        'view_title': 'Accueil'
    }

    if type(request) is not django.core.handlers.wsgi.WSGIRequest and request.user.is_authenticated:
        dico["nb_notif"] = request.user.notification_set.count()

    return render(request, 'index.html', dico)


def contactView(request):
    """Contact view

    Args:
        request (request): The request object needed by all views

    Returns:
        HttpResponseRedirect: A redirection to the home page if the user clicked on "send" in the form
        render: A render of the contact form
    """
    sent = False
    if request.method == 'POST':
        form = contactForm(request.POST)
        if form.is_valid():
            msg = Message()
            msg.subject = form.cleaned_data['sujet']
            msg.content = form.cleaned_data['message']
            msg.contact_mail = form.cleaned_data['envoyeur']
            msg.save()
            if not DEBUG:
                msg.send_as_mail(domain=request.META['HTTP_HOST'])
            else:
                messages.warning(request, "L'envoi d'email est désactivé sur cette platforme!")

            messages.add_message(
                request, messages.SUCCESS,
                "Votre message a bien été envoyé!")

            return HttpResponseRedirect(reverse("home"))

    else:
        form = contactForm()

    view_title = "Contact"
    return render(request, 'contact.html', locals())
