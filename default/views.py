# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib import messages

from default.models import Article, Message
from default.forms import contactForm


def home(request, param=""):
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
         }

    try:
        dico["nb_notif"] = request.user.notification_set.count()
    except Exception as e:
        print("Unauthenticated user :", e)

    return render(request, 'index.html', dico)


def contactView(request):
    sent = False
    if request.method == 'POST':
        form = contactForm(request.POST)
        if form.is_valid():
            sujet = form.cleaned_data['sujet']
            message = form.cleaned_data['message']
            envoyeur = form.cleaned_data['envoyeur']

            msg = Message()
            msg.subject = sujet
            msg.content = message
            msg.contact_mail = envoyeur
            msg.save()
            msg.send_as_mail()

            messages.add_message(
                request, messages.SUCCESS,
                "Votre message a bien été envoyé !")

            return HttpResponseRedirect("/")

    else:
        form = contactForm()

    return render(request, 'contact.html', locals())
