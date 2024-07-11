from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from .models import *
from django.utils.safestring import mark_safe
from django.http.response import Http404, HttpResponse
from django import forms
import csv
import io

def with_inline_organization_permissions(get_organization=lambda x: x):
    def deco(cls):
        class Admin(cls):
            def has_view_permission(self, request, obj=None):
                if obj is None or request.user.is_superuser:
                    return True
                org = get_organization(obj)
                return org.is_admin(request.user) or org.is_advisor(request.user)

            def has_change_permission(self, request, obj=None):
                return self.has_view_permission(request, obj)

            def has_add_permission(self, request, obj=None):
                return self.has_change_permission(request, obj)

            def has_delete_permission(self, request, obj=None):
                return self.has_change_permission(request, obj)

        return Admin

    return deco


def with_organization_permissions(get_organization=lambda x: x.organization, organization_field="organization"):
    def deco(cls):
        class Admin(cls):
            def has_module_permission(self, request):
                return True
            def has_view_permission(self, request, obj=None):
                if obj is None or request.user.is_superuser:
                    return True
                org = get_organization(obj)
                return org.is_admin(request.user) or org.is_advisor(request.user)
            def has_change_permission(self, request, obj=None):
                return self.has_view_permission(request, obj)
            def has_delete_permission(self, request, obj=None):
                return self.has_change_permission(request, obj)
            def get_queryset(self, request):
                qs = super().get_queryset(request)
                if request.user.is_superuser:
                    return qs
                return qs.filter(
                    Q(**{f"{organization_field}__admins": request.user})
                    | Q(**{f"{organization_field}__advisors": request.user})
                ).distinct()
            def get_form(self, request, obj=None, change=False, **kwargs):
                if not request.user.is_superuser:
                    form_class = cls.AdminAdvisorForm
                    class UserForm(form_class):
                        def __init__(self, *args, **kwargs):
                            super().__init__(*args, **kwargs)
                            q = Q(admins=request.user) | Q(advisors=request.user)
                            self.fields["organization"].queryset = (
                                self.fields["organization"].queryset.filter(q).distinct()
                            )
                    kwargs["form"] = UserForm
                return super().get_form(request, obj=obj, **kwargs)
        return Admin
    return deco



class AdminAdvisorListFilter(admin.SimpleListFilter):
    title = _("organization")

    parameter_name = "organization"

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            orgs = Organization.objects.all()
        else:
            orgs = Organization.objects.filter(Q(admins=request.user) | Q(advisors=request.user)).distinct()
            return [(org.id, org.name) for org in orgs]

    def queryset(self, request, queryset):
        return queryset.filter(organization=self.value())




@admin.register(User)
class UserAdmin(BaseUserAdmin, DynamicArrayMixin):
    class MembershipAdmin(admin.TabularInline, DynamicArrayMixin):
        model = Membership
        extra = 0

    class AdvisorOrganizationAdmin(admin.TabularInline, DynamicArrayMixin):
        model = Organization.advisors.through
        verbose_name = "Organization"
        verbose_name_plural = "Advisor For"
        extra = 0

    class AdminOrganizationAdmin(admin.TabularInline, DynamicArrayMixin):
        model = Organization.admins.through
        verbose_name = "Organization"
        verbose_name_plural = "Admin For"
        extra = 0

    class ExpoPushTokenAdmin(admin.TabularInline, DynamicArrayMixin):
        model = ExpoPushToken
        extra = 0


    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "type", "grad_year")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "grad_year", "password1", "password2")}),)
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "grad_year")
    search_fields = ("email", "first_name", "last_name")
    ordering = None
    inlines = (AdvisorOrganizationAdmin, AdminOrganizationAdmin, MembershipAdmin, ExpoPushTokenAdmin)

    def has_view_permission(self, request, obj=None):
        return True


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin, DynamicArrayMixin):
    class InlineLinkAdmin(admin.TabularInline, DynamicArrayMixin):
        model = OrganizationLink
        extra = 0

    class AdvisorForm(forms.ModelForm):
        class Meta:
            fields = (
                "advisors",
                "admins",
                "name",
                "description",
                "category",
                "day",
                "time",
                "link",
                "ical_links",
            )

    class AdminForm(forms.ModelForm):
        class Meta:
            fields = (
                "admins",
                "name",
                "description",
                "category",
                "day",
                "time",
                "location",
            )

    list_display = ("name", "type", "day", "time", "location")
    list_filter = ("type", "day")
    autocomplete_fields = ("advisors", "admins")
    inlines = (InlineLinkAdmin,)

    def has_module_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        if obj is None or request.user.is_superuser:
            return True
        return obj.is_admin(request.user) or obj.is_advisor(request.user)

    def has_change_permission(self, request, obj=None):
        return self.has_view_permission(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(admins=request.user) | Q(advisors=request.user)).distinct()
    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            kwargs["form"] = self.AdvisorForm if obj.is_advisor(request.user) else self.AdminForm
        return super().get_form(request, obj=obj, **kwargs)


@admin.register(Post)
@with_organization_permissions()
class PostAdmin(admin.ModelAdmin, DynamicArrayMixin):
    class AdminAdvisorForm(forms.ModelForm):
        class Meta:
            fields = ("organization", "title", "content", "published")

        def __init__(self, user, *args, **kwargs):
            super().__init__(*args, **kwargs)
            q = Q(admins=user) | Q(advisors=user)
            self.fields["organization"].queryset = self.fields["organization"].queryset.filter(q)

    date_hierarchy = "date"
    list_display = ("title", "date", "organization", "published")
    list_filter = ("organization", "published")
    list_editable = ("published",)

@admin.register(ExpoPushToken)
class ExpoPushTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token")
    search_fields = ("user__first_name", "user__last_name", "token")