from django.urls import include, path
from rest_framework_extensions.routers import ExtendedDefaultRouter

from . import views

router = ExtendedDefaultRouter()

users = router.register("users", views.UserViewSet, basename="core-user")
users.register("orgs", views.MembershipViewSet, basename="user-organization", parents_query_lookups=["user"])
router.register("orgs", views.OrganizationViewSet, basename="organization")
router.register("posts", views.PostViewSet, basename="post")

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.IndexView.as_view()),
]