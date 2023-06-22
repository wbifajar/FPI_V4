from django.shortcuts import render, redirect
from django.db import connection
from ..databaseConnect import *
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json

def Quotation(request):

    connection = connect()
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM quotation \
                    LEFT JOIN product ON quotation.Product_ID = product.idProduct \
                    LEFT JOIN customer ON quotation.Customer_ID = customer.idCustomer')
    quotation = cursor.fetchall()
    quotationjs = json.dumps(quotation, default=str)
    
    for item in quotation:
        item['Quantity'] = int(item['Quantity'])
        item['BudgetPerUnit'] = int(item['BudgetPerUnit'])
        item['total'] = int(item['Quantity']) * int(item['BudgetPerUnit'])
        item['expired'] = (item['CreatedAt']) + timedelta(days=10)

    context = {
        "quotation": quotation,
        "quotationjs": quotationjs,
    }

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete':
            selected_quotation_id = request.POST.get('selected_quotation')

            if selected_quotation_id:
                # Perform delete operation
                cursor.execute('DELETE FROM quotation WHERE Quotation_ID = %s', (selected_quotation_id,))
                connection.commit()

                # Reload the page after successful deletion
                return redirect('Quotation')

        elif action == 'edit':
            selected_quotation_id = request.POST.get('selected_quotation')

            if selected_quotation_id:
                # Retrieve the quotation data based on the selected ID
                cursor.execute('SELECT * FROM quotation WHERE Quotation_ID = %s', (selected_quotation_id,))
                quotation_data = cursor.fetchone()

                # Pass the quotation data to the template for pre-filling the form fields
                context['edit_quotation'] = quotation_data
    return render(request, 'quotation.html', context)




@login_required
def insertQuotation(request):
    if request.user.is_authenticated:
        username = request.user.username
        CustomerID = request.POST.get('customerid', False)
        ProductID = request.POST.get('productid', False)
        Quantity = request.POST.get('Quantity', False)
        BudgetPerUnit = request.POST['BudgetPerUnit']
        CostExcludeOperation = request.POST['CostExcludeOperation'].replace(',', '')
        OperationCost = request.POST['OperationCost']
        ManagementCostPercentage = request.POST['ManagementCostPercentage']
        MaterialCostNumber = request.POST['MaterialCostNumber']
        MaterialCostPercentage = request.POST['MaterialCostPercentage']
        OutsourceCostNumber = request.POST['OutsourceCostNumber']
        OutsourceCostPercentage = request.POST['OutsourceCostPercentage']
        OperationBudget = request.POST['OperationBudget'].replace(',', '')

        query = 'INSERT INTO Quotation VALUES ( null,"{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
            CustomerID,
            ProductID,
            Quantity,
            BudgetPerUnit,
            CostExcludeOperation,
            OperationCost,  
            ManagementCostPercentage,
            MaterialCostNumber,
            MaterialCostPercentage,
            OutsourceCostNumber,
            OutsourceCostPercentage,
            OperationBudget,
            timezone.now(),
            username,
        )
        print( "INSERRT QUERY = ", query)
        with connection.cursor() as cursor:
            cursor.execute(query)
        return redirect('/Quotation/')

def detailQuotation(request, quotation_id):
    if request.user.is_authenticated:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        query = 'SELECT * FROM quotation \
                        LEFT JOIN product ON quotation.Product_ID = product.idProduct \
                        LEFT JOIN customer ON quotation.Customer_ID = customer.idCustomer \
                       Where Quotation_ID = ' + str(quotation_id)
        cursor.execute(query)
        quotation = cursor.fetchall()
        quotationjs = json.dumps(quotation, default=str)

        print(quotation[0])
        context = {
            'q' : quotation[0],
            'quotation' : quotationjs[0]
        }

    return render(request, 'editquotation.html', context)