from django.test import TestCase
from django.contrib.auth.models import User

from default.models import Mail
import users.models as models

from administration.utils import thanksCoaches, sendNotifToCoaches


class UserTestCase(TestCase):
    """Tests different scenarios with users"""

    def setUp(self):
        """Sets up an environment for the tests to run in"""
        User.objects.create(username="a", first_name="user", last_name="etudiant")
        User.objects.create(username="b", first_name="user", last_name="coach")
        User.objects.create(username="c", first_name="user", last_name="coach2")
        User.objects.create(username="d", first_name="user", last_name="coach3")
        User.objects.create(username="e", first_name="user", last_name="coach4")

        student = models.Profile.objects.create(
            user=User.objects.get(username="a"), account_type="a"
        )
        student.Maths_course = True
        student.Francais_course = True
        student.school_level = "d"  # 3 ieme humanité
        student.save()
        models.StudentAccount.objects.create(profile=student)

        coach = models.Profile.objects.create(
            user=User.objects.get(username="b"), account_type="b"
        )
        coach.Maths_course = True
        coach.Chimie_course = True
        coach.school_level = "i"  # humanité
        coach.save()
        coach_account1 = models.CoachAccount.objects.create(profile=coach)
        coach_account1.confirmedAccount = "b"
        coach_account1.save()

        coach2 = models.Profile.objects.create(
            user=User.objects.get(username="c"), account_type="b"
        )
        coach2.Physique_course = True
        coach2.Chimie_course = True
        coach2.school_level = "j"  # humanité et primaire
        coach2.save()
        coach_account2 = models.CoachAccount.objects.create(profile=coach2)
        coach_account2.confirmedAccount = "b"
        coach_account2.save()

        coach3 = models.Profile.objects.create(
            user=User.objects.get(username="d"), account_type="b"
        )
        coach3.Francais_course = True
        coach3.Chimie_course = True
        coach3.school_level = "h"  # primaire seulement
        coach3.save()
        coach_account3 = models.CoachAccount.objects.create(profile=coach3)
        coach_account3.confirmedAccount = "b"
        coach_account3.save()

        coach4 = models.Profile.objects.create(
            user=User.objects.get(username="e"), account_type="b"
        )
        coach4.Francais_course = True
        coach4.Chimie_course = True
        coach4.school_level = "j"  # primaire seulement
        coach4.save()
        coach_account4 = models.CoachAccount.objects.create(profile=coach4)
        coach_account4.confirmedAccount = "b"
        coach_account4.save()

        Mail.objects.create(
            role="e",
            name="Mission trouvée",
            subject="On a trouvé une mission",
            content="Mission pour <STUDENT_FIRST_NAME> <STUDENT_LAST_NAME>"
        )

        Mail.objects.create(
            role="g",
            name="Dommaaage",
            subject="C'est pas pour toi mon pote",
            content="La mission de <STUDENT_FIRST_NAME> <STUDENT_LAST_NAME> elle est pas pour toi"
        )

    def test_student_request(self):
        """The requests notify the expected coaches"""
        student = User.objects.get(username="a")
        models.StudentRequest.objects.create(student=student)
        request = models.StudentRequest.objects.first()

        sendNotifToCoaches(request)

        coach1 = User.objects.get(username="b")
        coach2 = User.objects.get(username="c")
        coach3 = User.objects.get(username="d")
        coach4 = User.objects.get(username="e")

        self.assertEqual(coach1.notification_set.count(), 1)
        self.assertEqual(coach2.notification_set.count(), 0)
        self.assertEqual(coach3.notification_set.count(), 0)
        self.assertEqual(coach4.notification_set.count(), 1)

    def test_coach_accept(self):
        """The requests workflow to choose a coach works"""
        student = User.objects.get(username="a")
        models.StudentRequest.objects.create(student=student)

        coach1 = User.objects.get(username="b")
        coach2 = User.objects.get(username="c")
        coach3 = User.objects.get(username="d")
        coach4 = User.objects.get(username="e")

        # Make all the coaches 1 and 4 accept the request (they're the invited ones)
        student_request = models.StudentRequest.objects.get(student=student)
        student_request.coaches.add(coach1.profile.coachaccount)
        student_request.coaches.add(coach4.profile.coachaccount)
        student_request.save()

        request = models.StudentRequest.objects.get(student=student)
        coach = request.coaches.get(profile__user__username=coach1.username)
        other_coaches = request.coaches.all().exclude(
            profile__user__username=coach1.username
        )

        request.is_closed = True
        request.choosenCoach = coach
        student = student.profile.studentaccount
        student.coach = coach

        request.save()
        student.save()

        author = "L'équipe CAD"
        title = "Félicitations!"
        content = "Vous avez été choisi pour enseigner à {} {}! Vous pouvez \
        vous rendre sur votre profil pour retrouver les coordonées de cet \
        étudiant".format(
            student.profile.user.first_name, student.profile.user.last_name
        )
        models.Notification.objects.create(
            user=coach.profile.user, author=author, title=title, content=content
        )

        self.assertEqual(coach1.notification_set.count(), 1)
        self.assertEqual(coach2.notification_set.count(), 0)
        self.assertEqual(coach3.notification_set.count(), 0)
        self.assertEqual(coach4.notification_set.count(), 0)

        thanksCoaches(other_coaches, student)

        self.assertEqual(coach1.notification_set.count(), 1)
        self.assertEqual(coach2.notification_set.count(), 0)
        self.assertEqual(coach3.notification_set.count(), 0)
        self.assertEqual(coach4.notification_set.count(), 1)
