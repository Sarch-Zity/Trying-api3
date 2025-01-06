from django.urls import include, path
from . import views

urlpatterns = [
    path("auth/register", views.register, name="register"),
    path("auth/sign-in", views.signin, name="sign-in"),
    path("me/profile", views.me, name="me"),
]