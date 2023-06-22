from django.urls import path
from . import views

urlpatterns = [
    path('', views.Quotation, name='Quotation'),
    path('CreateNew/', views.CreateNewQuotation, name="CreateNew"),
    path('PDFQuotation/', views.PDFQuotation, name="PDFQuotation"),
    path('QuotationMaterial/', views.QuotationMaterial, name="QuotationMaterial"),
    path('tes-submit/', views.SubmitTest, name="TesSubmitForm"),
    path('insert-form/', views.InsertForm, name="InsertDB"),
    path('submittes/', views.insertQuotation, name="testes"),
    path('detail/<int:quotation_id>', views.detailQuotation, name="DetailQuotation")
] 