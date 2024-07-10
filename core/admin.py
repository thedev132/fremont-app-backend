from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from .models import *
import qrcode
from datauri import DataURI
from django.utils.safestring import mark_safe
from qrcode.image.svg import SvgPathFillImage

admin.site.site_header = "Fremont ASB"

@admin.register(User)
class UserAdmin(BaseUserAdmin, DynamicArrayMixin):
    class MembershipAdmin(admin.TabularInline, DynamicArrayMixin):
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
class OrganizationAdmin(admin.ModelAdmin, DynamicArrayMixin):
    class InlineLinkAdmin(admin.TabularInline, DynamicArrayMixin):
        model = OrganizationLink
        extra = 0
    list_display = ("name", "type", "day", "time", "link")
    list_filter = ("type", "day")
    inlines = (InlineLinkAdmin,)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin, DynamicArrayMixin):
    date_hierarchy = "date"
    list_display = ("title", "date", "organization", "published")
    list_filter = ("organization", "published")
    list_editable = ("published",)
    ordering = ("-date",)
