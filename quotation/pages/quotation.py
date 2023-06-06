from django.shortcuts import render, redirect
from django.db import connection
from ..databaseConnect import *
import json


def Quotation(request):
  connection = connect()
  cursor = connection.cursor(dictionary=True)
  cursor.execute('select * from quotation \
                 left join customer on quotation.Customer_ID = customer.idCustomer')
  quotation = cursor.fetchall()
  quotationjs = json.dumps(quotation, default=str)
  # print(quotation)

  for item in quotation:
    item['Quantity'] = int(item['Quantity'])
    item['BudgetPerUnit'] = int(item['BudgetPerUnit'])
    item['total'] = int(item['Quantity']) * int(item['BudgetPerUnit'])
    
  context = {
    "quotation" : quotation,
    "quotationjs" : quotationjs,
  }

  if request.method == 'POST':
    QuotationId = request.POST.get('QuotationId')


  return render(request, 'quotation.html', context)

def insertQuotation(request):

 
  # Customer_ID = 2
  # Product_ID = 2
  CustomerID = request.POST.get('customerid', False)
  ProductID = request.POST.get('productid', False)
  Quantity = request.POST.get('Quantity', False)  
  BudgetPerUnit = request.POST['BudgetPerUnit']
  # CostExcludeOperation = request.POST['CostExcludeOperation']
  # OperationCost = request.POST['OperationCost']
  # ManagementCostPercentage = request.POST['ManagementCostPercentage']
  # MaterialCostNumber = request.POST['MaterialCostNumber']
  # MaterialCostPercentage = request.POST['MaterialCostPercentage']
  # OutsorceCostNumber = request.POST['OutsorceCostNumber']
  # OutsorceCostPercentage = request.POST['OutsorceCostPercentage']
  # OperationBudget = request.POST['OperationBudget']
  

  # query = 'Insert Into Quotation values ( , "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", )'.format(
  #   Customer_ID,
  #   Product_ID,
  #   Quantity,
  #   BudgetPerUnit,
  #   CostExcludeOperation,
  #   OperationCost,
  #   ManagementCostPercentage,
  #   MaterialCostNumber,
  #   MaterialCostPercentage,
  #   OutsorceCostNumber,
  #   OutsorceCostPercentage,
  #   OperationBudget,
  # )

  
  query = 'Insert Into Quotation values ( NULL, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, CURRENT_TIMESTAMP)'.format(
    CustomerID,
    ProductID,
    Quantity,
    BudgetPerUnit,
    12,
    43,
    2,
    12,
    2,
    43,
    12,
    1,
  )

  with connection.cursor() as cursor:
    cursor.execute(query)
  return redirect('/Quotation/')