from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Organization, Post
from . import models

# Nested

class NestedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "first_name", "last_name")


class NestedOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = ("id", "name", "type")


class NestedMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Membership
        fields = ("organization", "points")

    organization = NestedOrganizationSerializer(read_only=True)

#Main

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "picture_url",
            "grad_year",
            "is_staff",
            "is_superuser",
            "memberships",
        )

    memberships = NestedMembershipSerializer(many=True, read_only=True)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = ("id", "url", "name", "type", "advisors", "admins", "day", "time", "link", "ical_links")

    advisors = NestedUserSerializer(many=True, read_only=True)
    admins = NestedUserSerializer(many=True, read_only=True)

class PostSerializer(serializers.ModelSerializer):
    class Meta:

        model = models.Post
        fields = ("id", "url", "organization", "title", "date", "content", "published", "polls")

    organization = NestedOrganizationSerializer(read_only=True)
