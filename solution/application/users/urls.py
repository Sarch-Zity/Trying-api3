from django.urls import include, path
from . import views

urlpatterns = [
    path("test", views.test, name="test"),
    path("auth/register", views.register, name="register"),
    path("auth/sign-in", views.signin, name="sign-in"),
    path("me/profile", views.me, name="me"),
    path("me/updatePassword", views.updatePassword, name="me"),
    path("profiles/<str:login>", views.profile, name="profile"),
]