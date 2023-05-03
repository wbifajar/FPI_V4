from django.urls import path
from . import views

urlpatterns = [
    path('', views.Quotation, name='Quotation'),
    path('CreateNew/', views.CreateNewQuotation, name="CreateNew"),
    path('PDFQuotation/', views.PDFQuotation, name="PDFQuotation"),
    path('QuotationMaterial/', views.QuotationMaterial, name="QuotationMaterial")
] 