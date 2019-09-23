from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from users.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    fk_name = "user"


class CoachAdmin(UserAdmin):

    list_display = (
        "username", "first_name", "last_name", "email", "account_type",
        "phone_number")
    list_filter = ("first_name", "last_name", "email")
    ordering = ("last_name", )
    search_fields = ("first_name", "last_name", "email")

    def account_type(self, instance):
        try:
            return instance.profile.account_type
        except Exception:
            return "Failed"

    def phone_number(self, instance):
        try:
            return instance.profile.phone_number
        except Exception:
            return "Failed"


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline]

    list_display = (
        "username", "account_type", "first_name", "last_name", "email")

    def account_type(self, instance):
        try:
            return instance.profile.account_type
        except Exception:
            return "failed"


admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)
