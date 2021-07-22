from django.shortcuts import render
from django.http import Http404


def old(request, name="index.htm"):
    """Renders a template from the old site

    Args:
        name (str, optional): The name of the template to render. Defaults to "index.htm".

    Raises:
        Http404: In case the template could not be found

    Returns:
        HttpResponse: The rendered template
    """
    if name[-1] == "/":
        name = name[:-1]
    try:
        return render(request, f"old_site/{name}")
    except Exception as e:
        print(name, "\n\n\n\n", e)
        raise Http404
