from django.urls import include, path
from . import views

urlpatterns = [
    path("new", views.new, name="new"),
    path("feed/<str:login>", views.feed, name="feed"),
    path("<str:id>", views.getbyid, name="getbyid"),
    path("<str:id>/like", views.like, name="like"),
    path("<str:id>/dislike", views.dislike, name="dislike"),
]