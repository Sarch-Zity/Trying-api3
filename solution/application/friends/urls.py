from django.urls import include, path
from . import views

urlpatterns = [
    path("add", views.add, name="add"),
    path("remove", views.remove, name="remove"),
    path("", views.friendslist, name="friendslist"),
]