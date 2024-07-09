from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class DayOfWeek(models.IntegerChoices):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class OrganizationType(models.IntegerChoices):
    GLOBAL = 1
    CLASS = 2
    CLUB = 3

class User(AbstractUser):
    pass


class Organization(models.Model):
    name = models.CharField(max_length=200)
    type = models.IntegerField(choices=OrganizationType.choices)
    advisors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="advisor_organization_set")
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="admin_organization_set")

    day = models.IntegerField(choices=DayOfWeek.choices)
    time = models.TimeField()
    link = models.URLField()

class Post(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    content = models.TextField()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)