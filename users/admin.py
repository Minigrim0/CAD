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
    list_display = (
        "user",
        "verifiedAccount",
        "courses",
    )
    list_filter = ("user", "verifiedAccount")
    ordering = ("user",)
    search_fields = ("user",)

    @staticmethod
    def courses(profile):
        return profile.courses


@admin.register(CoachAccount)
class CoachAdmin(admin.ModelAdmin):

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
    def first_name(coachaccount):
        return coachaccount.profile.user.first_name

    @staticmethod
    def last_name(coachaccount):
        return coachaccount.profile.user.last_name

    @staticmethod
    def email(coachaccount):
        return coachaccount.profile.user.email


@admin.register(StudentAccount)
class StudentAdmin(admin.ModelAdmin):

    list_display = ("first_name", "last_name", "email")

    @staticmethod
    def first_name(studentaccount):
        return studentaccount.profile.user.first_name

    @staticmethod
    def last_name(studentaccount):
        return studentaccount.profile.user.last_name

    @staticmethod
    def email(studentaccount):
        return studentaccount.profile.user.email


@admin.register(StudentRequest)
class StudentRequestAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "is_closed",
    )


@admin.register(FollowElement)
class FollowElementAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "coach", "date")
    list_filter = ("id", "student", "coach")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "amount", "admin", "date")
    list_filter = ("id", "student", "amount", "admin", "date")
