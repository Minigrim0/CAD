import datetime

from inscription.utils import sendNotifToCoaches
from users.models import studentRequest


def serializeDate(date_):
    """
        returns the date from "day month year" to "ddmmyyyy"
    """
    months = [
        "janvier",
        "février",
        "mars",
        "avril",
        "mai",
        "juin",
        "juillet",
        "aout",
        "septembre",
        "octobre",
        "novembre",
        "décembre"]
    date_ = date_.split()
    date_str = date_[0]
    if len(str(date_[0])) == 1:
        date_str = "0" + date_str

    if len(str(months.index(date_[1]) + 1)) == 1:
        date_str += "0" + str(months.index(date_[1]) + 1)
    else:
        date_str += str(months.index(date_[1]) + 1)

    date_str += str(date_[2])

    return datetime.datetime.strptime(date_str, "%d%m%Y")


def modifyStudent(profile, form):
    """
        Modifies a student profile according to the form given
    """
    sa = profile.studentaccount
    sa.NeedsVisit = False
    if form["Visit"] != "NoVisit":
        sa.NeedsVisit = True

    sa.comments = form["comments"]

    sa.tutor_firstName = form["tutorFirstName"]
    sa.tutor_name = form["tutorLastName"]

    if "confirmedAccount" in form.keys():
        if sa.confirmedAccount is False:
            sa.confirmedAccount = True
            # Continuer la procédure
            newRequest = studentRequest(student=profile.user)
            newRequest.save()

            sendNotifToCoaches(profile)
        else:
            sa.confirmedAccount = True
    else:
        sa.confirmedAccount = False
    sa.save()


def modifyCoach(profile, form):
    """
        Modifies a coach profile according to the form given
    """
    ca = profile.coachaccount

    ca.school = form["school"]
    ca.IBAN = form["IBAN"]
    ca.nationalRegisterID = form["natRegID"]

    ca.French_level = form["Frenchlevel"]
    ca.English_level = form["Englishlevel"]
    ca.Dutch_level = form["Dutchlevel"]

    ca.confirmedAccount = form["status"]
    ca.save()
