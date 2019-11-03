from django.contrib import admin
from users.models import StudentAccount, CoachAccount, studentRequest,\
    FollowElement


class CoachAdmin(admin.ModelAdmin):

    list_display = (
        "first_name", "last_name", "email", )
    list_filter = (
        "profile__user__first_name", "profile__user__last_name",
        "profile__user__email")
    ordering = ("profile__user__last_name", )
    search_fields = (
        "profile__user__first_name", "profile__user__last_name",
        "profile__user__email")

    def first_name(self, coachaccount):
        return coachaccount.profile.user.first_name

    def last_name(self, coachaccount):
        return coachaccount.profile.user.last_name

    def email(self, coachaccount):
        return coachaccount.profile.user.email


class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "first_name", "last_name", "email")

    def first_name(self, studentaccount):
        return studentaccount.profile.user.first_name

    def last_name(self, studentaccount):
        return studentaccount.profile.user.last_name

    def email(self, studentaccount):
        return studentaccount.profile.user.email


class StudentRequestAdmin(admin.ModelAdmin):
    list_display = (
        "student", "is_closed", )


class FollowElementAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'student', 'coach', 'date')
    list_filter = (
        "id", "student",
        "coach")


admin.site.register(StudentAccount, StudentAdmin)
admin.site.register(CoachAccount, CoachAdmin)
admin.site.register(studentRequest, StudentRequestAdmin)
admin.site.register(FollowElement, FollowElementAdmin)
