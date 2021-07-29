import logging

from django.shortcuts import render
from django.http import Http404


def old(request, name="index.html"):
    """Renders a template from the old site

    Args:
        name (str, optional): The name of the template to render. Defaults to "index.html".

    Raises:
        Http404: In case the template could not be found

    Returns:
        HttpResponse: The rendered template
    """
    if name[-1] == "/":
        name = name[:-1]

    try:
        return render(
            request, f"groups/{name}",
            context={
                "page_title": name[:-5]
            }
        )
    except Exception as e:
        logging.error(f"Accessing {name}\n{e}")
        raise Http404
