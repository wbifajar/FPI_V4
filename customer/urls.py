from django.urls import path
from . import views

app_name = "customer"
urlpatterns = [
    path('', views.Customer, name='Customer'),
    path('insert', views.insert, name='insert'),
    path("AddNewCustomer", views.AddNewCustomer, name="AddNewCustomer"),
    path("EditCustomer/<int:idCustomer>", views.EditCustomer, name="EditCustomer"),
    path("UpdateCustomer/<int:idCustomer>", views.UpdateCustomer, name="UpdateCustomer"),
    path("DeleteCustomer/<int:idCustomer>", views.DeleteCustomer, name="DeleteCustomer"),
] 