from django.urls import path

from . import views

app_name = "employee"
urlpatterns = [
    path("", views.index, name="index"),
    path("insert", views.insert, name="insert"),
    path("store", views.store, name="store"),
    path("edit/<int:employee_id>", views.edit, name="edit"),
    path("update/<int:employee_id>", views.update, name="update"),
    path("delete/<int:employee_id>", views.delete, name="delete"),
]