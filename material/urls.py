from django.urls import path
from . import views

app_name = 'material'
urlpatterns = [
    path('', views.index, name='Material'),
    path('insert', views.insert, name='insert'),
    path('store', views.store, name='InsertMaterial'),
    path("edit/<int:material_id>", views.edit, name="edit"),
    path("update/<int:material_id>", views.update, name="update"),
    path("delete/<int:material_id>", views.delete, name="delete"),
] 