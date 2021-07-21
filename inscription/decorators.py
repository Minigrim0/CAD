from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse


def mustnt_be_logged_in(action="inscrire"):
    """A decorator indicating the user should be anonymous to access the content

    Args:
        action (str, optional): The action the user is trying to do. Defaults to "inscrire".
    """

    def decorator(func: callable):
        """The decorator in itself

        Args:
            func (callable): [description]
        """

        def wrapper(*args, **kwargs):
            """The wrapper of the function

            Returns:
                ?: The result of the wrapped function
            """
            request = args[0]
            if request.user.is_authenticated:
                messages.warning(
                    request,
                    f"Vous êtes connecté en tant que {request.user.first_name} {request.user.last_name},\
                        si vous souhaitez vous {action} avec un autre compte, déconnectez-vous d'abord !",
                )
                return HttpResponseRedirect(reverse("home"))
            return func(*args, **kwargs)

        return wrapper

    return decorator
