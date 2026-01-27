from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, login_view, register

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("users/register/", register, name="register"),
    path("users/login/", login_view, name="login"),
    path("", include(router.urls)),
]
