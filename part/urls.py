from django.urls import path

from . import views

app_name = "part"
urlpatterns = [
    path("", views.part, name="index"),
]