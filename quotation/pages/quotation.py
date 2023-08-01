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
                    LEFT JOIN customer ON quotation.Customer_ID = customer.idCustomer \
                   ORDER BY QUOTATION_ID DESC') #untuk sementara aja urutin dari yg paling baru
    quotation = cursor.fetchall()
    quotationjs = json.dumps(quotation, default=str)
    
    for item in quotation:
        item['QUANTITY'] = int(item['QUANTITY'])
        item['BUDGET_PER_UNIT'] = int(item['BUDGET_PER_UNIT'])
        item['TOTAL'] = int(item['QUANTITY']) * int(item['BUDGET_PER_UNIT'])
        item['EXPIRED'] = (item['CREATED_AT']) + timedelta(days=10)

    context = {
        "quotation": quotation,
        "quotationjs": quotationjs,
    }

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete':
            selected_quotation_id = request.POST.getlist('selected_quotation')

            if selected_quotation_id:
                # Perform delete operation
                for i in range (0, len(selected_quotation_id)):
                    query = 'DELETE FROM quotation WHERE Quotation_ID = ' + selected_quotation_id[i]
                    cursor.execute(query)
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
    quotation_id = quotation[0]["QUOTATION_ID"]
    return quotation_id

def handleEmptyString(val, default_value_if_empty):
    if val == '':
        return default_value_if_empty
    return val

def insertQuotationMaterial(request):
    # ========== Quotation Material ==========
    BoardArr = request.POST['BoardArr'].split(',')
    BarArr = request.POST['BarArr'].split(',')
    
    QUOTATION_ID = getLastCreatedQuotationID()

    MaterialList = request.POST.getlist('material_id')
    MaterialLength = len(MaterialList)
    if(MaterialLength == 0) : return

    print(MaterialLength)
    USED_QUANTITY = request.POST.getlist('usedQuantity')
    BoardArrView = [BoardArr[i:i+29] for i in range(0, len(BoardArr), 29)]
    BarArrView = [BarArr[i:i+27] for i in range(0, len(BarArr), 29)]
    for item in BoardArrView:
        print("BOARDARR = ", item )
    for item in BarArrView:
        print("BARARR = ", item )
    
    for i in range(0, MaterialLength):
        MaterialID = MaterialList[i]
        UsedQuantity = handleEmptyString(USED_QUANTITY[i], 0)
        BoardVerticalScale = handleEmptyString(BoardArr[i * 29 + 3], 0) #1
        BoardHorizontalScale = handleEmptyString(BoardArr[i * 29 + 4], 0) #2
        BoardThickness = handleEmptyString(BoardArr[i * 29 + 5], 0) #3
        BoardVerticalScaleFromNumber = handleEmptyString(BoardArr[i * 29 + 8], 0) #4
        BoardHorizontalScaleFromNumber = handleEmptyString(BoardArr[i * 29 + 9], 0) #5
        BoardExposedFromNumber = handleEmptyString(BoardArr[i * 29 + 10], 0) #6
        BoardMarginFromNumber = handleEmptyString(BoardArr[i * 29 + 11], 0) #7
        BoardMaterialCostFromNumber = handleEmptyString(BoardArr[i * 29 + 20], 0) #8
        BoardExposedFromPartScale = handleEmptyString(BoardArr[i * 29 + 22], 0) #9
        BoardMarginFromPartScale = handleEmptyString(BoardArr[i * 29 + 23], 0) #10
        BarPartScalp = handleEmptyString(BarArr[i * 27 + 12], 0) #11
        BarDiameter = handleEmptyString(BarArr[i * 27 + 4], 0) #12
        BarExposed = handleEmptyString(BarArr[i * 27 + 7], 0) #13
        BarLength = handleEmptyString(BarArr[i * 27 + 8], 0) #14
        BarEdgeLoss = handleEmptyString(BarArr[i * 27 + 9], 0) #15
        BarKeftLoss = handleEmptyString(BarArr[i * 27 + 15], 0) #16
        query =  'INSERT INTO quotation_material VALUES ( null, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(
            QUOTATION_ID,
            MaterialID,
            UsedQuantity,
            BoardVerticalScale, 
            BoardHorizontalScale,
            BoardThickness,
            BoardVerticalScaleFromNumber,
            BoardHorizontalScaleFromNumber,
            BoardExposedFromNumber,
            BoardMarginFromNumber, 
            BoardMaterialCostFromNumber, 
            BoardExposedFromPartScale,
            BoardMarginFromPartScale, 
            BarPartScalp,
            BarDiameter,
            BarExposed,
            BarLength,
            BarEdgeLoss,
            BarKeftLoss,
        )
        print( "MaterialList = ", query )
        with connection.cursor() as cursor:
            cursor.execute(query)
    print('=============================================================')

    print('asddsadd')

def insertQuotationProcess(request):
    QUOTATION_ID = getLastCreatedQuotationID()

    ProcessId = request.POST.getlist('ProcessId')
    ProcessLength = len(ProcessId)
    Opesum = request.POST.getlist('opeSum')
    OpePerOpeBudgetRatio = request.POST.getlist('operationPerOperationBudgetRatio')
    OpePerBudgetRatio = request.POST.getlist('operationPerBudgetRatio')
    SetTime = request.POST.getlist('setTime')
    OpeTime = request.POST.getlist('opeTime')
    TotalOpeTime = request.POST.getlist('totalOpeTime')
    QuantityPerMin = request.POST.getlist('quantityPerMinute')

    print("ORICIANISBIFBSAIBF")
    print(ProcessId)
    print("QPM = ", QuantityPerMin)
    for i in range(0, ProcessLength):
       
        # UsedQuantity = handleEmptyString(USED_QUANTITY[i], 0)
        # Opesum = handleEmptyString()
    
        query = 'INSERT INTO quotation_process VALUES (null, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
            QUOTATION_ID,
            ProcessId[i],
            # UsedQuantity[i],
            Opesum[i],
            OpePerOpeBudgetRatio[i],
            OpePerBudgetRatio[i],
            SetTime[i],
            OpeTime[i],
            TotalOpeTime[i],
            QuantityPerMin[i],
        )
        print(query)
        with connection.cursor() as cursor:
            cursor.execute(query)

def insertQuotationOther(request):
    QUOTATION_ID = getLastCreatedQuotationID()
    
    OtherId = request.POST.getlist('othersId')
    OtherLength = len(OtherId)
    OtherPrice = request.POST.getlist('otherprice')
    OtherPercentage = request.POST.getlist('otherpercentage')

    perUnit_Arr = []
    for i in range(0, OtherLength):
        OtherIsPerUnit = request.POST.get(f'otherisperunit-{i+1}', False)
       
        if OtherIsPerUnit == "on":
            perUnit_Arr.append(1)
        else:
            perUnit_Arr.append(0)

        # ni print buat ngecek doang
        print("Orderisperunit = ", perUnit_Arr, OtherIsPerUnit)

    # OtherIsPerUnit = [1 if value == 'on' else 0 for value in OtherIsPerUnit]

    for i in range(0, OtherLength):
        query = 'INSERT INTO quotation_other VALUES (null, "{}", "{}", "{}", "{}", "{}")'.format(
            QUOTATION_ID,
            OtherId[i],
            OtherPrice[i],
            OtherPercentage[i],
            perUnit_Arr[i],
        )
        with connection.cursor() as cursor:
            cursor.execute(query)



@login_required
def insertQuotation(request):
    if request.user.is_authenticated:
        CustomerID = request.POST.get('customerid', False)
        ProductID = request.POST.get('productid', False)
        ProductName = request.POST.get('productname', False)
        ProductVersion = request.POST.get('productver', False)
        Quantity = request.POST.get('Quantity', False)
        BudgetPerUnit = request.POST['BudgetPerUnit']
        CostExcludeOperation = float(request.POST.get('MaterialOutsourceOtherCost', False).replace(",", "") )
        OperationCost = float(request.POST.get('TotalOperationCost', False))
        ManagementCostPercentage = request.POST['ManagementCostPercentage']
        MaterialCostNumber = request.POST['MaterialCostNumber']
        MaterialCostPercentage = request.POST['MaterialCostPercentage']
        OutsourceCostNumber = request.POST['OutsourceCostNumber']
        OutsourceCostPercentage = request.POST['OutsourceCostPercentage']
        OperationBudget = request.POST['OperationBudget'].replace(',', '')
        Username = request.user.username
        Status = request.POST.get('quotation_status', False)
        print("STATUS = ", Status)

        query = 'INSERT INTO Quotation VALUES ( null, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
            CustomerID,
            ProductID,
            ProductName,
            ProductVersion,
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
            Username,
            Status
        )
        
        print( "INSERT QUERY = ", query)
        with connection.cursor() as cursor:
            cursor.execute(query)

        insertQuotationProcess(request)
        insertQuotationOther(request)
        insertQuotationMaterial(request)

        return redirect('/Quotation/')

def detailQuotation(request, quotation_id):
    if request.user.is_authenticated:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        query = 'SELECT * FROM quotation \
                        LEFT JOIN customer ON quotation.Customer_ID = customer.idCustomer \
                       Where Quotation_ID = ' + str(quotation_id)
        cursor.execute(query)
        quotation = cursor.fetchall()
        quotation = quotation[0]
        quotationjs = json.dumps(quotation, default=str)

        quotation["QUANTITY"] = int(quotation["QUANTITY"])
        totalBudget = quotation["QUANTITY"] * quotation["BUDGET_PER_UNIT"]
        totalCost = quotation["COST_EXCLUDE_OPERATION"] + quotation["OPERATION_COST"]
        managementCost = quotation["BUDGET_PER_UNIT"] * 0.3
        # totalMaterialCost =  quotation["MATERIAL_COST_NUMBER"] * ( quotation["MATERIAL_COST_PERCENTAGE"] / 100 )
        # totalOutsourceCost = quotation["OUTSOURCE_COST_NUMBER"] * ( quotation["OUTSOURCE_COST_PERCENTAGE"] / 100 )
        
        query = 'SELECT * fROM quotation_material \
                LEFT JOIN PART ON PART.idPART = QUOTATION_MATERIAL.MATERIAL_ID \
                WHERE Quotation_ID = ' + str(quotation_id)
        
        cursor.execute(query)
        material = cursor.fetchall()
        materialjs = json.dumps(material, default=str)
        
        for item in material:
            item["MATERIAL_COST"] = float(item["USED_QUANTITY"]) * item["price"]
            print(item)
       

            
        cursor.execute('select * from part')
        part = cursor.fetchall()
        partjs = json.dumps(part)

        query = 'SELECT * FROM quotation_material \
                LEFT JOIN PART ON PART.idPART = QUOTATION_MATERIAL.MATERIAL_ID \
                WHERE Quotation_ID = ' + str(quotation_id)
        
        cursor.execute(query)
        selected_material = cursor.fetchall()
        selected_material_js = json.dumps(selected_material)
        print("SELECTED_MATERIAL ====> ", selected_material_js)

        # detail process
        query = 'select * from quotation_process JOIN PROCESS ON QUOTATION_PROCESS.PROCESS_ID = PROCESS.ProcessID where Quotation_ID = ' + str(quotation_id)
                
        cursor.execute(query)
        quotation_process = cursor.fetchall()
        quotation_process_js = json.dumps(quotation_process)
        print(quotation_process)

        # detail other
        queryOther = 'select * from quotation_other JOIN OTHER ON quotation_other.OTHER_ID = OTHER.OtherId where Quotation_ID =' + str(quotation_id)
        cursor.execute(queryOther)
        quotation_other = cursor.fetchall()
        quotation_other_js = json.dumps(quotation_other)

        # context
        context = { 
            'q' : quotation,
            'quotation' : quotationjs,
            'TotalBudget' : totalBudget,
            'TotalCost' : totalCost,
            "ManagementCost" : managementCost,
          
            'material' : material,
            'materialjs' : materialjs,

            'partreflectcost' : part,
		    'partreflectcostjs' : partjs,

            'selected_material' : selected_material,
            'selected_material_js' : selected_material_js,

            'quotation_process' : quotation_process,
            'quotation_process_js' : quotation_process_js,

            'quotation_other' : quotation_other,
            'quotation_other_js' : quotation_other_js,
        }

    return render(request, 'editquotation.html', context)


def insertProcess(request):
    QUOTATION_ID = getLastCreatedQuotationID()

    ProcessId = request.POST.getlist('ProcessId')
    ProcessLength = len(ProcessId)
    # Quantity = request.POST.getlist('usedQuantity')

    
    Opesum = request.POST.getlist('opeSum')
    OpePerOpeBudgetRatio = request.POST.getlist('operationPerOperationBudgetRatio')
    OpePerBudgetRatio = request.POST.getlist('operationPerBudgetRatio')
    SetTime = request.POST.getlist('setTime')
    OpeTime = request.POST.getlist('opeTime')
    TotalOpeTime = request.POST.getlist('totalOpeTime')
    QuantityPerMin = request.POST.getlist('quantityPerMinute')

    print(Opesum)
 
    print("ASDSDSAD = ", QuantityPerMin)
    for i in range(0, ProcessLength):
       
        # UsedQuantity = handleEmptyString(USED_QUANTITY[i], 0)
        # Opesum = handleEmptyString()
    
        query = 'INSERT INTO quotation_process VALUES (null, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
            QUOTATION_ID,
            ProcessId[i],
            # UsedQuantity[i],
            Opesum[i],
            OpePerOpeBudgetRatio[i],
            OpePerBudgetRatio[i],
            SetTime[i],
            OpeTime[i],
            TotalOpeTime[i],
            QuantityPerMin[i],
        )
        with connection.cursor() as cursor:
            cursor.execute(query)

    # insertQuotationMaterial(request)
    # return redirect('/Quotation/')