from django.urls import path

from . import views

app_name = "group"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:group_id>/permission", views.group_permission, name="group_permission"),
    path("<int:group_id>/permission/edit", views.edit_group_permission, name="edit_group_permission"),
    path("<int:group_id>/permission/update", views.update_group_permission, name="update_group_permission"),
    path("<int:group_id>/users", views.group_user, name="group_user"),
]