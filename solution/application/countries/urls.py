from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.countries, name="countires"),
    path("<str:alpha2>/", views.countriesalpha, name="countires"),
]