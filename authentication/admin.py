from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from authentication.models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password", "auth_provider")}),
        (_("Personal info"), {"fields": ("full_name", "image", "face",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "role",
                    "is_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "full_name", "role", "auth_provider", "image", "face", "password1", "password2")}),
    )
    list_display = ("email", "full_name", "role", "auth_provider", "is_verified", "is_staff")
    search_fields = ("email", "full_name")
    ordering = ("email",)
    list_filter = ('role', 'is_verified',)


admin.site.register(CustomUser, CustomUserAdmin)
