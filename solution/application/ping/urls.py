from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.ping, name="ping"),
]