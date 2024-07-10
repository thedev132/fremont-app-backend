from django.contrib.auth import get_user_model
from rest_framework import viewsets

# Create your views here.
from .models import Organization
from .serializers import OrganizationSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer