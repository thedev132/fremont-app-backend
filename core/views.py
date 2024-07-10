from django.contrib.auth import get_user_model
from rest_framework import filters, pagination, views, viewsets
from django.views.generic.base import TemplateView

from . import models, serializers

class IndexView(TemplateView):
    template_name = "index.html"

class SmallPages(pagination.PageNumberPagination):
    page_size = 20


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.OrganizationSerializer

    def get_queryset(self):
        if "clubs" in self.request.query_params:
            return models.Organization.objects.filter(type=3)
        if "user" in self.request.query_params:
            return models.Organization.objects.filter(users=self.request.user)
        return models.Organization.objects.all()


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PostSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = ("-date",)
    pagination_class = SmallPages

    def get_queryset(self):
        return models.Post.objects.filter(organization__users=self.request.user)
