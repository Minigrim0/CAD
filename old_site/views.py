from django.shortcuts import render
from django.http import Http404


def old(request, name="index.htm"):
    if name[-1] == "/":
        name = name[:-1]
    try:
        return render(request, f"old_site/{name}")
    except Exception as e:
        print(name, "\n\n\n\n", e)
        raise Http404
