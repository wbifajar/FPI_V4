from django.urls import path

from . import views

app_name = "part"
urlpatterns = [
    path("", views.index, name="index"),
    path("insert", views.insert, name="insert"),
    path("store", views.store, name="store"),
    path("edit/<int:idPart>", views.edit, name="edit"),
    path("update/<int:idPart>", views.update, name="update"),
    path("delete/<int:idPart>", views.delete, name="delete"),
]