# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from default.models import Article
from default.forms import contactForm


def home(request, param=""):
    home = Article.objects.filter(name="Accueil")
    info = Article.objects.filter(name="Info")
    video = Article.objects.filter(name="Video")
    coaches = Article.objects.filter(name="Coaches")
    about = Article.objects.filter(name="About")
    contact = Article.objects.filter(name="Contact")

    dico_ = {'a_home':    home[0],
             'a_info':    info[0],
             'a_video':   video[0],
             'a_coaches': coaches[0],
             'a_about':   about[0],
             'a_contact': contact[0],
             'a_Success': [],
             'a_Failed': []}

    if param == "01":
        dico_["a_Success"].append(
            "Votre compte a bien été créé ! Vous recevrez un mail sous peu \
            pour confirmer la création de votre compte")
    elif param == "02":
        dico_["a_Failed"].append("Il y a eu une erreur lors de la création de \
        votre compte, réessayez plus tard")
    elif param == "03":
        dico_["a_Success"].append("Rebonjour " + request.user.first_name)
    elif param == "04":
        dico_["a_Failed"].append("Vos identifiants ne correspondent à \
        aucun compte !")
    elif param == "05":
        dico_["a_Failed"].append("Une erreur est survenue lors du chargement \
        de la page")
    elif param == "06":
        dico_["a_Failed"].append("Vous avez été déconnecté")
    elif param == "07":
        dico_["a_Failed"].append("L'utilisateur a été supprimé")
    elif param == "08":
        dico_["a_Success"].append("Votre message a bien été envoyé")
    elif param == "09":
        dico_["a_Failed"].append("Une erreur est survenue lors de l'envoi de \
        votre message, réessayez plus tard")
    elif param == "10":
        dico_["a_Failed"].append("Votre paiement a été annulé, n'oubliez pas \
        de le compléter au plus vite, afin de pouvoir commencer a suivre des \
        cours avec nos coaches !")
    elif param == "11":
        dico_["a_Success"].append("Merci d'avoir complété votre inscription ! \
        Nous allons de ce pas chercher un coach pour vous !")
    elif param == "12":
        dico_["a_Failed"].append("Votre compte à été suspendu. reconnectez \
        vous pour annuler la suppression")
    elif param == "13":
        dico_["a_Success"].append("Votre compte à bien été confirmé ! Vous \
        allez pouvoir commencer à donner cours !")
    elif param == "14":
        dico_["a_Failed"].append("Vous avez déjà confirmé votre compte !")

    try:
        dico_["nb_notif"] = request.user.notification_set.count()
    except Exception as e:
        print("Unauthenticated user :", e)

    return render(request, 'index.html', dico_)


def contactView(request):
    sent = False
    if request.method == 'POST':
        form = contactForm(request.POST)
        if form.is_valid():
            sujet = form.cleaned_data['sujet']
            message = form.cleaned_data['message']
            envoyeur = form.cleaned_data['envoyeur']

            return HttpResponseRedirect("/08/")

    else:
        form = contactForm()

    return render(request, 'contact.html', locals())
