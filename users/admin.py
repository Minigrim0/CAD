from django.contrib import admin
from users.models import (
    StudentAccount,
    CoachAccount,
    StudentRequest,
    FollowElement,
    Transaction,
    Profile,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """The admin of the profile model"""

    list_display = (
        "user",
        "verifiedAccount",
        "courses",
    )
    list_filter = ("user", "verifiedAccount")
    ordering = ("user",)
    search_fields = ("user",)

    @staticmethod
    def courses(profile: Profile) -> str:
        """Shows the course given or seeked by a profile"""
        return profile.courses


@admin.register(CoachAccount)
class CoachAdmin(admin.ModelAdmin):
    """The admin of the coach account model"""

    list_display = (
        "first_name",
        "last_name",
        "email",
    )
    list_filter = (
        "profile__user__first_name",
        "profile__user__last_name",
        "profile__user__email",
    )
    ordering = ("profile__user__last_name",)
    search_fields = (
        "profile__user__first_name",
        "profile__user__last_name",
        "profile__user__email",
    )

    @staticmethod
    def first_name(coachaccount: CoachAccount) -> str:
        """Shows the first name of the coach account"""
        return coachaccount.profile.user.first_name

    @staticmethod
    def last_name(coachaccount: CoachAccount) -> str:
        """Shows the last name of the coach account"""
        return coachaccount.profile.user.last_name

    @staticmethod
    def email(coachaccount: CoachAccount) -> str:
        """Shows the email address of the coach account"""
        return coachaccount.profile.user.email


@admin.register(StudentAccount)
class StudentAdmin(admin.ModelAdmin):
    """The admin of the student account model"""

    list_display = ("first_name", "last_name", "email")

    @staticmethod
    def first_name(studentaccount):
        """Shows the first name of the student account"""
        return studentaccount.profile.user.first_name

    @staticmethod
    def last_name(studentaccount):
        """Shows the last name of the student account"""
        return studentaccount.profile.user.last_name

    @staticmethod
    def email(studentaccount):
        """Shows the email of the student account"""
        return studentaccount.profile.user.email


@admin.register(StudentRequest)
class StudentRequestAdmin(admin.ModelAdmin):
    """The admin of the student request model"""

    list_display = (
        "student",
        "is_closed",
    )


@admin.register(FollowElement)
class FollowElementAdmin(admin.ModelAdmin):
    """The admin of the follow element model"""

    list_display = ("id", "student", "coach", "date")
    list_filter = ("id", "student", "coach")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """The admin of the transaction model"""

    list_display = ("id", "student", "amount", "admin", "date")
    list_filter = ("id", "student", "amount", "admin", "date")
