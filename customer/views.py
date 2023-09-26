from django.shortcuts import render

from django.db import connection
from django.http import HttpResponse

import json

def Customer(request):
  return render(request, 'customer.html')

def AddNewCustomer(request):
  return render(request, 'addcustomer.html')

def EditCustomer(request):
  return render(request, 'editcustomer.html')

# Create your views here.