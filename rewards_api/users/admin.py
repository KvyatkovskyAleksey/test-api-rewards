from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ScheduledReward, RewardLog, UserRewardRequest
from django.utils.translation import gettext_lazy as _


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "coins", "is_staff")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("Additional Info"), {"fields": ("coins",)}),
    )


@admin.register(ScheduledReward)
class ScheduledRewardAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "execute_at")
    search_fields = ("user__username",)
    list_filter = ("execute_at",)


@admin.register(RewardLog)
class RewardLogAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "given_at")
    search_fields = ("user__username",)
    list_filter = ("given_at",)


@admin.register(UserRewardRequest)
class UserRewardRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "date")
    search_fields = ("user__username",)
    list_filter = ("date",)
