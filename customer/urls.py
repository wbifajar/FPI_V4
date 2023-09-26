from django.urls import path
from . import views

urlpatterns = [
    path('', views.Customer, name='Customer'),
    path('AddNewCustomer/', views.AddNewCustomer, name="AddNewCustomer"),
    path('EditCustomer/', views.EditCustomer, name="EditCustomer"),

    # path('line-graph/', views.line_graph, name='line_graph'),
] 