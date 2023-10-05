from django.urls import path

from . import views

app_name = "user"
urlpatterns = [
    path("", views.index, name="index"),
    path("insert", views.insert, name="insert"),
    path("store", views.store, name="store"),
]