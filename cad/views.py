from django.shortcuts import render


def chooseLocation(request):
    return render(request, "chooseLocation.html")
