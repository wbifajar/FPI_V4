from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.db import connection
from .databaseConnect import *

@permission_required('customer.view_customer', raise_exception=True)
def index(request):

    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM CUSTOMER'
    cursor.execute( query )
    res = cursor.fetchall()

    context = {
        'customer' : res, 
    }

    return render(request, 'customer_index.html', context)
    # return HttpResponse(res)

@permission_required('customer.add_customer', raise_exception=True)
def insert(request):
  return render(request, 'customer_insert.html')


def store(request):
  CustomerStatus = request.POST.get('customerStatus')
  CustomerName = request.POST.get('customerName', False)
  CustomerTaxID = request.POST.get('customerTaxID', False)
  CustomerPIC = request.POST.get('customerPIC', False)
  CustomerTlp1 = request.POST.get('customerTlp', False)
  CustomerTlp2 = request.POST.get('customerTlp1', False)
  CustomerAddress1 = request.POST.get('customerAddress', False)
  CustomerAddress2 = request.POST.get('customerAddress1', False)
  CustomerZipCode = request.POST.get('customerZipCode', False)
  print(CustomerStatus)

  query = f'INSERT INTO customer VALUES(null, "{CustomerStatus}", "{CustomerName}", "{CustomerTaxID}", "{CustomerPIC}", "{CustomerTlp1}", "{CustomerTlp2}", "{CustomerAddress1}", "{CustomerAddress2}", "{CustomerZipCode}")'

  with connection.cursor() as cursor:
    cursor.execute(query)
  return redirect('/customer')

@permission_required('customer.change_customer', raise_exception=True)
def edit(request, idCustomer):
  connection = connect()
  cursor = connection.cursor(dictionary=True)
  query = 'SELECT * FROM customer WHERE idCustomer = ' + str(idCustomer)

  cursor.execute( query )
  customer = cursor.fetchall()

  context = {
    'customer' : customer[0], 
  }

  return render(request, 'customer_edit.html', context)

def update(request, idCustomer):
  CustomerStatus = request.POST.get('customerStatus', False)
  CustomerName = request.POST.get('customerName', False)
  CustomerTaxID = request.POST.get('customerTaxID', False)
  CustomerPIC = request.POST.get('customerPIC', False)
  CustomerTlp1 = request.POST.get('customerTlp', False)
  CustomerTlp2 = request.POST.get('customerTlp1', False)
  CustomerAddress1 = request.POST.get('customerAddress', False)
  CustomerAddress2 = request.POST.get('customerAddress1', False)
  CustomerZipCode = request.POST.get('customerZipCode', False)
  query = f'UPDATE customer \
      SET \
      customerStatus = "{CustomerStatus}", \
      customerName = "{CustomerName}", \
      customerTaxID = "{CustomerTaxID}", \
      customerPIC = "{CustomerPIC}", \
      customerTlp = "{CustomerTlp1}", \
      customerTlp1 = "{CustomerTlp2}", \
      customerAddress = "{CustomerAddress1}", \
      customerAddress1 = "{CustomerAddress2}", \
      customerZipCode = "{CustomerZipCode}"\
      WHERE idCustomer = "{idCustomer}"'
  
  print(query)

  with connection.cursor() as cursor:
      cursor.execute(query)
  return redirect('/customer')

@permission_required('customer.delete_customer', raise_exception=True)
def delete(request, idCustomer):
    query = f'DELETE FROM customer WHERE idCustomer = {idCustomer}'
    with connection.cursor() as cursor:
        cursor.execute(query)

    return redirect('/customer')