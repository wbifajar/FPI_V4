from django.urls import path

from . import views

app_name = "other"
urlpatterns = [
    path("", views.index, name="index"),
    path("insert", views.insert, name="insert"),
    path("store", views.store, name="store"),
    path("edit/<int:OtherId>", views.edit, name="edit"),
    path("update/<int:OtherId>", views.update, name="update"),
    path("delete/<int:OtherId>", views.delete, name="delete"),
]