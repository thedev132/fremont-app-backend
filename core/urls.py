from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
#router.register("users", views.UserViewSet)
router.register("orgs", views.OrganizationViewSet)
router.register("posts", views.PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]