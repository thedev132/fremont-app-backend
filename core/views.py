from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.views.generic.base import TemplateView
from rest_framework import filters, mixins, pagination, status, views, viewsets
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from core.permissions import NestedUserAccessPolicy, UserAccessPolicy

from . import models, serializers


class IndexView(TemplateView):
    template_name = "core/index.html"

class RedirectView(TemplateView):
    template_name = "core/redirect.html"
class SmallPages(pagination.PageNumberPagination):
    page_size = 20


class NestedUserViewSetMixin(NestedViewSetMixin):
    def get_parents_query_dict(self):
        kw = super().get_parents_query_dict()
        for key in ("user", "users"):
            if kw.get(key) == "me":
                kw[key] = self.request.user.id
        return kw

    def get_user(self):
        qdict = self.get_parents_query_dict()
        for key in ("user", "users"):
            try:
                user_id = qdict[key]
                break
            except KeyError:
                pass
        else:
            return None
        return get_user_model().objects.get(pk=user_id)


class UserViewSet(viewsets.ReadOnlyModelViewSet, mixins.UpdateModelMixin):
    permission_classes = (UserAccessPolicy,)
    serializer_class = serializers.UserSerializer

    @property
    def access_policy(self):
        return self.permission_classes[0]
    def get_object(self):
        if self.kwargs.get("pk") == "me":
            self.kwargs["pk"] = self.request.user.id
        return super().get_object()
    def get_queryset(self):
        qs = get_user_model().objects.all()
        if self.action == "list":
            return self.access_policy.scope_queryset(self.request, qs)
        else:
            return qs
        

class ExpoPushTokenViewSet(
    NestedUserViewSetMixin, viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    permission_classes = (NestedUserAccessPolicy,)
    queryset = models.ExpoPushToken.objects.all()
    serializer_class = serializers.ExpoPushTokenSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.get_user())


class MembershipViewSet(
    NestedUserViewSetMixin, viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin
):
    permission_classes = (NestedUserAccessPolicy,)
    queryset = models.Membership.objects.filter(active=True)
    lookup_field = "organization"

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.CreateMembershipSerializer
        return serializers.MembershipSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.get_user())

    def perform_destroy(self, instance):
        instance.active = False
        instance.save()

    def handle_exception(self, exc):
        if isinstance(exc, IntegrityError):
            return Response(status=status.HTTP_409_CONFLICT)
        return super().handle_exception(exc)


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.OrganizationSerializer

    def get_queryset(self):
        if "clubs" in self.request.query_params:
            # TODO: Deprecated. Remove when app is updated.
            return models.Organization.objects.filter(type=3)

        if "user" in self.request.query_params:
            # TODO: Deprecated. Remove when app is updated.
            return models.Organization.objects.filter(users=self.request.user)

        return models.Organization.objects.all()
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PostSerializer
    pagination_class = SmallPages
    def get_queryset(self):
        return models.Post.objects.filter(published=True, organization__users=self.request.user)

class AppVersionView(views.APIView):
    permission_classes = ()
    
    def get(self, r):
        return Response({"android": 1, "ios": "1.0"})