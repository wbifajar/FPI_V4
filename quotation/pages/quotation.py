from django.shortcuts import render, redirect

def Quotation(request):
  
  if request.method == 'POST':
    QuotationId = request.POST.get('QuotationId')

  return render(request, 'quotation.html')

def insertQuotation(request):

 
  Customer_ID = request.POST['Customer_ID']
  Product_ID = request.POST['Product_ID']
  Quantity = request.POST['quantity']
  BudgetPerUnit = request.POST['BudgetPerUnit']
  CostExcludeOperation = request.POST['CostExcludeOperation']
  OperationCost = request.POST['OperationCost']
  ManagementCostPercentage = request.POST['ManagementCostPercentage']
  MaterialCostNumber = request.POST['MaterialCostNumber']
  MaterialCostPercentage = request.POST['MaterialCostPercentage']
  OutsorceCostNumber = request.POST['OutsorceCostNumber']
  OutsorceCostPercentage = request.POST['OutsorceCostPercentage']
  OperationBudget = request.POST['OperationBudget']
  

  query = 'Insert Into Quotation values ( , "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "")'.format(
    Customer_ID,
    Product_ID,
    Quantity,
    BudgetPerUnit,
    CostExcludeOperation,
    OperationCost,
    ManagementCostPercentage,
    MaterialCostNumber,
    MaterialCostPercentage,
    OutsorceCostNumber,
    OutsorceCostPercentage,
    OperationBudget,
  )
  return redirect('/quotation')