from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Material'),
    path('insert-material', views.InsertForm, name='InsertMaterial'),
] 