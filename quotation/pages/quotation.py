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
                    JOIN product ON quotation.Product_ID = product.idProduct \
                    JOIN customer ON quotation.Customer_ID = customer.idCustomer')
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

def getLastCreatedQuotationID():
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM QUOTATION ORDER BY QUOTATION_ID DESC LIMIT 1"
    cursor.execute(query)

    quotation = cursor.fetchall()
    quotation_id = quotation[0]["Quotation_ID"]
    return quotation_id

def insertQuotationMaterial(request):
    BoardArr = request.POST['BoardArr']
    BarArr = request.POST['BarArr']
    
    QUOTATION_ID = getLastCreatedQuotationID()

    MaterialList = request.POST.getlist('material_id')
    MaterialLength = len(MaterialList)
    print(MaterialLength)
    USED_QUANTITY = request.POST.getlist('usedQuantity')
    
    BOARD_VERTICAL_SCALE = 0 #1
    BOARD_HORIZONTAL_SCALE = 0 #2
    BOARD_THICKNESS = 0 #3
    BOARD_VERTICAL_SCALE_FROM_NUMBER = 0 #4
    BOARD_HORIZONTAL_SCALE_FROM_NUMBER = 0 #5
    BOARD_EXPOSED_FROM_NUMBER = 0 #6
    BOARD_MARGIN_FROM_NUMBER = 0 #7
    BOARD_MATERIAL_COST_FROM_NUMBER = 0 #8
    BOARD_EXPOSED_FROM_PART_SCALE = 0 #9
    BOARD_MARGIN_FROM_PART_SCALE = 0 #10
    BAR_PART_SCALP = 0 #11
    BAR_DIAMETER = 0 #12
    BAR_EXPOSED = 0 #13
    BAR_LENGTH = 0 #14
    BAR_EDGE_LOSS = 0 #15
    BAR_KEFT_LOSS = 0 #16
    
    for i in range(0, MaterialLength):
        # query =  'INSERT INTO quotation_material VALUES ( null, 32, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)'
        query =  'INSERT INTO quotation_material VALUES ( null, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(
            QUOTATION_ID,
            MaterialList[i],
            USED_QUANTITY[i],
            BoardArr[i][3], #verscale
            BoardArr[i][4],
            BoardArr[i][5],
            BoardArr[i][8],
            BoardArr[i][9],
            BoardArr[i][10],
            BoardArr[i][11], #7
            BoardArr[i][20], #8
            BoardArr[i][22],
            BoardArr[i][23],
            BarArr[i][12],
            BarArr[i][4],
            BarArr[i][7],
            BarArr[i][8],
            BarArr[i][9],
            BarArr[i][15],
            
        )
        with connection.cursor() as cursor:
            cursor.execute(query)
    print( "MaterialList = ", MaterialList, BoardArr)
    print('=============================================================')


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
        print( "INSERT QUERY = ", query)
        with connection.cursor() as cursor:
            cursor.execute(query)

        insertQuotationMaterial(request)
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
        quotation = quotation[0]
        quotationjs = json.dumps(quotation, default=str)

        totalBudget = quotation["Quantity"] * quotation["BudgetPerUnit"]
        totalCost = quotation["CostExcludeOperation"] + quotation["OperationCost"]
        managementCost = quotation["BudgetPerUnit"] * 0.3
        totalMaterialCost =  quotation["MaterialCostNumber"] * ( quotation["MaterialCostPercentage"] / 100 )
        totalOutsourceCost = quotation["OutsorceCostNumber"] * ( quotation["OutsorceCostPercentage"] / 100 )
        
        query = 'SELECT * fROM quotation_material \
                JOIN PART ON PART.idPART = QUOTATION_MATERIAL.MATERIAL_ID \
                WHERE Quotation_ID = ' + str(quotation_id)
        cursor.execute(query)
        material = cursor.fetchall()
        materialjs = json.dumps(material, default=str)

        context = {
            'q' : quotation,
            'quotation' : quotationjs[0],
            'TotalBudget' : totalBudget,
            'TotalCost' : totalCost,
            "ManagementCost" : managementCost,
            "TotalMaterialCost" : totalMaterialCost,
            "TotalOutsourceCost" :  totalOutsourceCost,

            'material' : material,
            'materialjs' : materialjs
        }

    return render(request, 'editquotation.html', context)