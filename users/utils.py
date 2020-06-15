from users.models import Notification


def thanksCoaches(coaches, student):
    author = "L'équipe CAD"
    title = "Merci d'avoir répondu présent"
    content = "Merci d'avoir répondu présent à la requête de {} {}. \
    Malheureusement, vous n'avez pas été choisit pour donner cours à \
    cet étudiant. Mais ne vous en faites pas, voitre tour viendra !".format(
        student.first_name, student.last_name)
    for coach in coaches:
        new_notif = Notification(
            user=coach.user,
            author=author,
            title=title,
            content=content)
        new_notif.save()
