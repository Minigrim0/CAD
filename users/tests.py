from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile, StudentAccount, CoachAccount, Notification, Transaction


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="a", first_name="user", last_name="etudiant")
        User.objects.create(username="b", first_name="user", last_name="coach")

        student = Profile.objects.create(user=User.objects.get(username="a"), account_type="a")
        student.Maths_course = True
        student.Francais_course = True
        student.save()
        StudentAccount.objects.create(profile=student)

        coach = Profile.objects.create(user=User.objects.get(username="b"), account_type="b")
        coach.Maths_course = True
        coach.Chimie_course = True
        coach.save()
        CoachAccount.objects.create(profile=coach)

    def test_user_courses(self):
        """Animals that can speak are correctly identified"""
        student = User.objects.get(username="a")
        coach = User.objects.get(username="b")
        self.assertEqual(student.profile.courses, 'Maths, Francais')
        self.assertEqual(coach.profile.courses, 'Maths, Chimie, ')

    def test_user_notification(self):
        """Animals that can speak are correctly identified"""
        student = User.objects.get(username="a")
        notif = Notification.objects.create(user=student)
        notif.title = "Title"
        notif.content = "content"
        notif.author = "sender"
        notif.save()

        self.assertEqual(student.notification_set.count(), 1)

    def test_student_balance(self):
        """Animals that can speak are correctly identified"""
        student = User.objects.get(username="a")
        
        transaction = Transaction.objects.create(student=student.profile.studentaccount)
        transaction.amount = 20
        transaction.save()

        self.assertEqual(student.profile.studentaccount.balance, 20)

        transaction = Transaction.objects.create(student=student.profile.studentaccount)
        transaction.amount = -10
        transaction.save()

        self.assertEqual(student.profile.studentaccount.balance, 10)
