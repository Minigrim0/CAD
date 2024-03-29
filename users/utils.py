from users.models import CoachAccount, StudentRequest, Notification


def findRequestsForCoach(coach: CoachAccount):
    """Finds opened request fitting the coach

    Args:
        coach (CoachAccount): The coach for whom to find requests
    """
    requests = StudentRequest.objects.filter(is_closed=False)
    available_requests = []
    for request in requests:
        if coach.profile.isCompatible(request.student.profile):
            available_requests.append(request)

    newNotif = Notification(user=coach.profile.user)
    newNotif.author = "L'équipe CAD"

    newNotif.title = "Nous avons trouvé une liste de missions disponibles pour vous"
    newNotif.content = "Vous pouvez visiter les missions ci-dessous afin de commencer votre parcours de coach ! <ul>"
    newNotif.content += "".join(
        f"<li><a href='{request.fullUrl}'>{request.student.first_name} {request.student.last_name}</a></li>"
        for request in available_requests
    )
    newNotif.content += "</ul>"

    newNotif.save()
    newNotif.send_as_mail()
    coach.save()
