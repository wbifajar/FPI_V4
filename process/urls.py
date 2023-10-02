from django.urls import path

from . import views

app_name = "process"
urlpatterns = [
    path("", views.index, name="index"),
    path("edit/<int:process_id>", views.edit, name="edit"),
    path("update/<int:process_id>", views.update, name="update"),
]