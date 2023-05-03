from django.shortcuts import render

from .pages.quotation import *
from .pages.newQuotation import *
# Create your views here.

Quotation

CreateNewQuotation

def PDFQuotation(request):
  return render(request, 'pdfquotation.html')


def QuotationMaterial(request):
  return render(request, 'quotationmaterial.html')
