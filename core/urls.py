from django.urls import include, path
from rest_framework_extensions.routers import ExtendedDefaultRouter

from . import views

router = ExtendedDefaultRouter()

users = router.register("users", views.UserViewSet, basename="core-user")
users.register("orgs", views.MembershipViewSet, basename="user-organization", parents_query_lookups=["user"])
users.register("tokens", views.ExpoPushTokenViewSet, basename="user-token", parents_query_lookups=["user"])

router.register("orgs", views.OrganizationViewSet, basename="organization")
router.register("posts", views.PostViewSet, basename="post")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/app_version/", views.AppVersionView.as_view()),
    path("", views.IndexView.as_view()),
    path("redirect/", views.RedirectView.as_view()),
]