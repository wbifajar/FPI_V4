from django.shortcuts import render, redirect
from django.db import connection
from ..databaseConnect import *

def Quotation(request):
  
  if request.method == 'POST':
    QuotationId = request.POST.get('QuotationId')

  return render(request, 'quotation.html')

def insertQuotation(request):

 
  # Customer_ID = 2
  # Product_ID = 2
  Quantity = request.POST.get('quantity', False)  
  # BudgetPerUnit = request.POST['BudgetPerUnit']
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
    1,
    4,
    4,
    100,
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