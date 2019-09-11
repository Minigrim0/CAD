from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
import datetime

@staff_member_required
def adminPage(request):
    users = User.objects.all()
    firstUser = users[0].username

    level_ = {'5' : 'Langue maternelle',
              '4' : 'Très bon',
              '3' : 'Bon',
              '2' : 'Notions de base',
              '1' : 'Aucun'}

    lang_ = {'French'  : 'Francais',
             'Dutch'   : 'Néerlandais',
             'English' : 'Anglais'}

    vars_ = {'a_users' : users, 'a_firstUserUsername' : firstUser, "i_langLevel" : level_, "i_lang" : lang_}

    return render(request, 'admin/admin.html', vars_)

@staff_member_required
def reactivate(request, string=""):
    if string == "":
        return HttpResponseRedirect("/05/")

    usr = User.objects.get(username=string)
    usr.is_active = True
    usr.save()
    return HttpResponseRedirect("/administration")


def serializeDate(date_):
    """
        returns the date from "day month year" to "ddmmyyyy"
    """
    months = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "décembre"]
    date_ = date_.split()
    date_str = date_[0]
    if len(str(date_[0])) == 1:
        date_str = "0" + date_str

    if len(str(months.index(date_[1])+1)) == 1:
        date_str += "0" + str(months.index(date_[1])+1)
    else:
        date_str += str(months.index(date_[1])+1)

    date_str += str(date_[2])

    return datetime.datetime.strptime(date_str, "%d%m%Y")

@staff_member_required
def modifyUser(request):
    if request.method == "POST": #Check if the way the user accessed this url is correct
        try:
            form = request.POST
            if "modify" in form.keys(): #If the admin wants to modify the user
                usr = User.objects.get(username=form["username"])
                usr.first_name = form["firstName"]
                usr.last_name  = form["lastName"]
                usr.email      = form["mail"]
                usr.save() #Saves basic user model

                try: #Checks if the user as a profile extension
                    type = usr.profile.account_type #Get account type to try

                    #Modifications that apply for ll type of account
                    usr.profile.phone_number = form["phone_number"]
                    usr.profile.address      = form["address"]
                    usr.profile.birthDate    = serializeDate(form["birthDate"])

                    for course in ["Maths", "Chimie", "Physique", "Francais"]:
                        if course+"_Course" in form.keys():
                            exec("usr.profile." + course + "_course = True")
                        else:
                            exec("usr.profile." + course + "_course = False")

                    if type == "Etudiant": #Modifications that only apply to student type account
                        usr.profile.wanted_schedule = ""
                        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
                            id = "course " + day
                            try:
                                if form[id] == 'on':
                                    usr.profile.wanted_schedule += "1/"
                                    usr.profile.wanted_schedule += form[day+"Start"] + "/"
                                    usr.profile.wanted_schedule += form[day+"End"]   + "."
                            except:
                                usr.profile.wanted_schedule += "0/0/0."

                        usr.profile.NeedsVisit = False
                        if form["Visit"] != "NoVisit":
                            usr.profile.NeedsVisit = True

                        usr.profile.comments = form["comments"]

                        usr.profile.tutor_firstName = form["tutorFirstName"]
                        usr.profile.tutor_name      = form["tutorName"]
                    elif type == "Coach": #Modifications that only apply to coach type account
                        usr.profile.school             = form["school"]
                        usr.profile.IBAN               = form["IBAN"]
                        usr.profile.nationalRegisterID = form["natRegID"]

                        usr.profil.French_level  = form["Frenchlevel"]
                        usr.profil.English_level = form["Englishlevel"]
                        usr.profil.Dutch_level   = form["Dutchlevel"]

                    usr.profile.save() #Saving the profile extension model

                except Exception as e: #If the user as no profile extension
                    print("Error :", e) #Print the error in case it's not because the user has no profile

                return HttpResponseRedirect("/administration") #Redirect to administration
            elif "reactivate" in form.keys():
                print("user is reactive")
                return HttpResponseRedirect("/administration/reactivate/"+form["username"])
            else: #If the admin wants to 'delete' the user
                usr = User.objects.get(username=form["username"])
                if usr.is_active:
                    usr.is_active = False #Deactivate the user's account
                    usr.save()
                else:
                    print("user deleted")
                    usr.delete() #Completely deletes it
                return HttpResponseRedirect("/administration")
        except Exception as e: #In case an error occurs
            print(e) #Print it
            return HttpResponseRedirect('/administration')
    else:
        return HttpResponseRedirect('/administration')
