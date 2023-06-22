from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from .pages.quotation import *
from .pages.newQuotation import *

from django.db import connection

import json
# Create your views here.

Quotation

CreateNewQuotation

def PDFQuotation(request):
  return render(request, 'pdfquotation.html')


def QuotationMaterial(request):
  return render(request, 'quotationmaterial.html')

def SubmitTest(request):
  connection = connect()
  cursor = connection.cursor(dictionary=True)
  query = "Select * from part"
  cursor.execute(query)
  res = cursor.fetchall()
  print('==================================================================================', res)
  context = {
    "Parts" : res
  }
  

  template = loader.get_template('submitTest.html')
  return HttpResponse(template.render(context, request))

def InsertForm(request):
  nama = request.POST['nama']
  gravity = request.POST['gravity']
  price = request.POST['price']
  with connection.cursor() as cursor:
    query = 'Insert Into Part values (null, "{}", {}, {})'.format(nama, gravity, price)
    cursor.execute( query )
  return redirect('/Quotation/tes-submit')

