from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def connexion(request):
    if request.method != "POST":
        return render(request, 'connexion.html', locals())
    else:
        form = request.POST
        email = form["coMail"]
        password = form["coPass"]

        try:
            user = User.objects.get(email=email)  # Get user obj via its email
            user = authenticate(username=user.username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect("/03/")
        except Exception as e:
            print("Error : ", e)

        return HttpResponseRedirect("/04/")