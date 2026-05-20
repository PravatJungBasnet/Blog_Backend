from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ["email", "first_name", "last_name", "is_staff"]
    list_filter = ["is_staff"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    ("first_name", "last_name"),
                    "profile_picture",
                    ("email"),
                    "password",
                    ("is_staff", "is_active", "password_set"),
                    "groups",
                ]
            },
        ),
    ]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["-email"]

    def delete_queryset(self, request, queryset):
        for user in queryset:
            user.delete()

    def get_queryset(self, request):
        return User.all_objects.all()

    @admin.action(description="Restore selected users")
    def restore_user(self, request, queryset):
        restored_account = 0
        for user in queryset:
            if user.deleted_at:
                user.restore()
                restored_account += 1

        self.message_user(request, f"{restored_account} user(s) successfully restored.")

    actions = ["restore_user"]
