from django.urls import path

from . import views

app_name = "process"
urlpatterns = [
    path("", views.index, name="index"),
    path("insert", views.insert, name="insert"),
    path("store", views.store, name="store"),
    path("edit/<int:process_id>", views.edit, name="edit"),
    path("update/<int:process_id>", views.update, name="update"),
    path("delete/<int:process_id>", views.delete, name="delete"),
    path("insertCategory", views.insertCategory, name="insertCategory"),
    path("storeCategory", views.storeCategory, name="storeCategory"),
    path("editCategory/<int:category_id>", views.editCategory, name="editCategory"),
    path("updateCategory/<int:category_id>", views.updateCategory, name="updateCategory"),
]