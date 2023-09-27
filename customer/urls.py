from django.urls import path
from . import views

app_name = "customer"
urlpatterns = [
    path('', views.index, name='index'),
    path('insert', views.insert, name='insert'),
    path("store", views.store, name="store"),
    path("edit/<int:idCustomer>", views.edit, name="edit"),
    path("update/<int:idCustomer>", views.update, name="update"),
    path("delete/<int:idCustomer>", views.delete, name="delete"),
] 