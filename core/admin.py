from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from .models import *


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    class MembershipAdmin(admin.StackedInline, DynamicArrayMixin):
        model = Membership
        extra = 0

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "grad_year")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "grad_year", "password1", "password2")}),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "grad_year")
    search_fields = ("email", "first_name", "last_name")
    ordering = None
    inlines = (MembershipAdmin,)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "day", "time", "link")
    list_filter = ("type", "day")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    list_display = ("title", "date", "organization", "published")
    list_filter = ("organization", "published")
    list_editable = ("published",)
    ordering = ("-date",)
