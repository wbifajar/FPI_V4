from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.db import connection
from .databaseConnect import *

def Customer(request):
  connection = connect()
  cursor = connection.cursor(dictionary=True)

  query = 'select * from customer'
  cursor.execute( query )
  customer = cursor.fetchall()

  context = {
      'customer' : customer, 
  }
  return render(request, 'customer.html', context)

def insert(request):
  return render(request, 'addcustomer.html')

def AddNewCustomer(request):
  addCustomerStatus = request.POST.get('addCustomerStatus', False)
  addCustomerName = request.POST.get('addCustomerName', False)
  addCustomerTaxID = request.POST.get('addCustomerTaxID', False)
  addCustomerPIC = request.POST.get('addCustomerPIC', False)
  addCustomerTlp1 = request.POST.get('addCustomerTlp1', False)
  addCustomerTlp2 = request.POST.get('addCustomerTlp2', False)
  addCustomerAddress1 = request.POST.get('addCustomerAddress1', False)
  addCustomerAddress2 = request.POST.get('addCustomerAddress2', False)
  addCustomerZipCode = request.POST.get('addCustomerZipCode', False)

  query = f'INSERT INTO customer VALUES(null, "{addCustomerStatus}", "{addCustomerName}", "{addCustomerTaxID}", "{addCustomerPIC}", "{addCustomerTlp1}", "{addCustomerTlp2}", "{addCustomerAddress1}", "{addCustomerAddress2}", "{addCustomerZipCode}")'

  with connection.cursor() as cursor:
    cursor.execute(query)
  return redirect('/customer')

def EditCustomer(request, idCustomer):
  connection = connect()
  cursor = connection.cursor(dictionary=True)
  query = 'SELECT * FROM customer WHERE idCustomer = ' + str(idCustomer)

  cursor.execute( query )
  customer = cursor.fetchall()

  context = {
    'customer' : customer[0], 
  }

  return render(request, 'editcustomer.html', context)

def UpdateCustomer(request, idCustomer):
  addCustomerStatus = request.POST.get('addCustomerStatus', False)
  addCustomerName = request.POST.get('addCustomerName', False)
  addCustomerTaxID = request.POST.get('addCustomerTaxID', False)
  addCustomerPIC = request.POST.get('addCustomerPIC', False)
  addCustomerTlp1 = request.POST.get('addCustomerTlp1', False)
  addCustomerTlp2 = request.POST.get('addCustomerTlp2', False)
  addCustomerAddress1 = request.POST.get('addCustomerAddress1', False)
  addCustomerAddress2 = request.POST.get('addCustomerAddress2', False)
  addCustomerZipCode = request.POST.get('addCustomerZipCode', False)
  query = f'UPDATE customer \
      SET \
      addCustomerStatus = "{addCustomerStatus}", \
      addCustomerName = "{addCustomerName}", \
      addCustomerTaxID = "{addCustomerTaxID}" \
      addCustomerPIC = "{addCustomerPIC}", \
      addCustomerTlp1 = "{addCustomerTlp1}", \
      addCustomerTlp2 = "{addCustomerTlp2}" \
      addCustomerAddress1 = "{addCustomerAddress1}", \
      addCustomerAddress2 = "{addCustomerAddress2}", \
      addCustomerZipCode = "{addCustomerZipCode}" \
      WHERE idCustomer = "{idCustomer}"'
  
  print(query)

  with connection.cursor() as cursor:
      cursor.execute(query)
  return redirect('/customer')

def DeleteCustomer(request, idCustomer):
    query = f'DELETE FROM customer WHERE idCustomer = {idCustomer}'
    with connection.cursor() as cursor:
        cursor.execute(query)

    return redirect('/customer')