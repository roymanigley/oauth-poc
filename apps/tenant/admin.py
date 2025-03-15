from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.tenant.models import Tenant


class TenantAdmin(UserAdmin):
    list_display = ("id", "name", "is_staff", "is_active")
    search_fields = ("id", "name",)
    ordering = ("name",)

    fieldsets = (
        (None, {"fields": ("name", "password")}),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("name", "password1", "password2"),
        }),
    )


admin.site.register(Tenant, TenantAdmin)
