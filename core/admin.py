from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Organization, Post, User


admin.site.register(User, UserAdmin)


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