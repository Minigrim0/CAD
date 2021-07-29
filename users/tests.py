from django.test import TestCase
from django.contrib.auth.models import User

import users.models as models


class UserTestCase(TestCase):
    """Tests things related to the user models"""

    def setUp(self):
        """Sets up an environment for the tests to occur"""
        User.objects.create(username="a", first_name="user", last_name="etudiant")
        User.objects.create(username="b", first_name="user", last_name="coach")

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

    def test_student_balance(self):
        """The student's balance is correctly calculated"""
        student = User.objects.get(username="a")

        transaction = models.Transaction.objects.create(
            student=student.profile.studentaccount
        )
        transaction.amount = 20
        transaction.save()

        self.assertEqual(student.profile.studentaccount.balance, 20)

        transaction = models.Transaction.objects.create(
            student=student.profile.studentaccount
        )
        transaction.amount = -10
        transaction.save()

        self.assertEqual(student.profile.studentaccount.balance, 10)

    def test_user_courses(self):
        """User courses render correctly"""
        student = User.objects.get(username="a")
        coach = User.objects.get(username="b")
        self.assertEqual(student.profile.courses, "Maths, Francais")
        self.assertEqual(coach.profile.courses, "Maths, Chimie, ")

    def test_user_notification(self):
        """User correctly receives notification"""
        student = User.objects.get(username="a")
        notif = models.Notification.objects.create(user=student)
        notif.title = "Title"
        notif.content = "content"
        notif.author = "sender"
        notif.save()

        self.assertEqual(student.notification_set.count(), 1)
