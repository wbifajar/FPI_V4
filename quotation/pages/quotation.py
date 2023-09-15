from django.shortcuts import render, redirect
from django.db import connection
from ..databaseConnect import *
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
import json

def Quotation(request):
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM quotation \
                LEFT JOIN customer ON quotation.Customer_ID = customer.idCustomer \
                WHERE IS_ACTIVE = 1 \
                ORDER BY QUOTATION_ID DESC')  # untuk sementara aja urutin dari yg paling baru

    quotation = cursor.fetchall()

    # Modify and calculate values for each quotation
    for item in quotation:
        item['QUANTITY'] = int(item['QUANTITY'])
        item['BUDGET_PER_UNIT'] = int(item['BUDGET_PER_UNIT'])
        item['TOTAL'] = int(item['QUANTITY']) * int(item['BUDGET_PER_UNIT'])
        item['EXPIRED'] = (item['CREATED_AT']) + timedelta(days=14)
        item['QUOTATION_ID'] = item['QUOTATION_ID']
        item['QUOTATION_STATUS'] = item['QUOTATION_STATUS']
        item['expired_date'] = str(item['expired_date'])


    # Extract only the required fields for JSON serialization
    # quotation_data = [{'QUOTATION_ID': q['QUOTATION_ID'], 'QUOTATION_STATUS': q['QUOTATION_STATUS']} for q in quotation]

    # Serialize quotation data to JSON
    # quotationjs = json.dumps(quotation_data, default=str)

    # Extract only the required fields for JSON serialization
    quotation_data = [{'QUOTATION_ID': q['QUOTATION_ID'], 'QUOTATION_STATUS': q['QUOTATION_STATUS']} for q in quotation]

    # Serialize quotation data to JSON
    quotationjs = json.dumps(quotation_data, default=str)

    context = {
        "quotation": quotation,
        "quotationjs": quotationjs,
    }

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete':
            selected_quotation_ids = request.POST.getlist('selected_quotation')

            if selected_quotation_ids:
                for i in range (0, len(selected_quotation_ids)-1):
                  
                    query = 'UPDATE QUOTATION SET IS_ACTIVE = 0 WHERE QUOTATION_ID = ' + selected_quotation_ids[i]
                    print(query)
                    cursor.execute(query)
                    connection.commit()
                # Reload the page after successful deletion
                return redirect('/Quotation')
        elif action == 'createPDF':
            selected_quotation_ids = request.POST.getlist('selected_quotation')
            pdf_data = []
    
            if selected_quotation_ids:
                # Fetch the customer name of the first selected quotation
                cursor.execute('SELECT Customer_Name FROM quotation WHERE Quotation_ID = %s', (selected_quotation_ids[0],))
                customer_name = cursor.fetchone()

                if customer_name:
                    customer_name = customer_name['Customer_Name']
                    
                    # Retrieve the quotation data for selected IDs with the same customer name
                    placeholders = ','.join(['%s'] * len(selected_quotation_ids))  # Create placeholders for parameterized query
                    query = '''
                        SELECT *
                        FROM quotation
                        LEFT JOIN product ON quotation.Product_ID = product.idProduct
                        LEFT JOIN customer ON quotation.Customer_ID = customer.idCustomer
                        WHERE Quotation_ID IN ({}) AND Customer_Name = %s
                    '''.format(placeholders)
                    
                    cursor.execute(query, selected_quotation_ids + [customer_name])
                    pdf_data = cursor.fetchall()
                
                context['pdf_quotation'] = pdf_data

        elif action == 'copyQuotation':
            selected_quotation_id = request.POST.getlist('selected_quotation')
         
    return render(request, 'quotation.html', context)


def createPDFQuotation(request, quotation_id):
    if request.user.is_authenticated:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        selected_ids = quotation_id.split(',')  # Split the comma-separated IDs
        placeholders = ','.join(['%s'] * len(selected_ids))  # Create placeholders for parameterized query
        query = '''
            SELECT *
            FROM quotation
            LEFT JOIN product ON quotation.Product_ID = product.idProduct
            LEFT JOIN customer ON quotation.Customer_ID = customer.idCustomer
            WHERE Quotation_ID IN ({})
        '''.format(placeholders)

        cursor.execute(query, selected_ids)
        quotations = cursor.fetchall()
       
        from datetime import timedelta

        if quotations:
            quotation = quotations[0]  # You might want to process each quotation if there are multiple

            quantity = int(quotation['QUANTITY'])
            budgetPerUnit = int(quotation['BUDGET_PER_UNIT'])
            expired = quotation['CREATED_AT'] + timedelta(days=10)
            expiredFormat = expired.strftime("%d/%m/%Y")
            createdAtFormat = quotation['CREATED_AT'].strftime("%d/%m/%Y")
            
            # Calculate amount for each quotation and store them in a list
            amount_list = [(qpdf['QUANTITY'] * qpdf['BUDGET_PER_UNIT']) for qpdf in quotations]

            subtotal = sum(amount_list)
            ppn = int(subtotal * 0.11)
            total = int(subtotal + ppn)

            # Zip qs and amount_list together
            zipped_data = zip(quotations, amount_list)

            context = {
                'q': quotation,
                'zipped_data': zipped_data,  # Pass the zipped data to the template
                'expired': expired,
                'expiredFormat': expiredFormat,
                'createdAtFormat': createdAtFormat,
                'quantity': quantity,
                'budgetPerUnit': budgetPerUnit,
                'subtotal': subtotal,
                'ppn': ppn,
                'total': total,
            }

            return render(request, 'pdfquotation.html', context)

    return HttpResponse('Unauthorized', status=401)  # Return an appropriate response for unauthorized users


def getLastCreatedQuotationID():
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM QUOTATION ORDER BY QUOTATION_ID DESC LIMIT 1"
    cursor.execute(query)

    quotation = cursor.fetchall()
    quotation_id = quotation[0]["QUOTATION_ID"]
    return quotation_id

def handleEmptyString(val , default_value_if_empty):
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
        print("QUOATION PROCESS query = ", query)
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
        CostExcludeOperation = float(request.POST.get('MaterialOutsourceOtherCost', False).replace(",", ""))
        OperationCost = float(request.POST.get('TotalOperationCost', False))
        ManagementCostPercentage = request.POST['ManagementCostPercentage']
        MaterialCostNumber = request.POST['MaterialCostNumber']
        MaterialCostPercentage = request.POST['MaterialCostPercentage']
        OutsourceCostNumber = request.POST['OutsourceCostNumber']
        OutsourceCostPercentage = request.POST['OutsourceCostPercentage']
        OperationBudget = request.POST['OperationBudget'].replace(',', '')
        Username = request.user.username
        Status = request.POST.get('quotation_status', False)
        # Generate QuotationNo
        today = timezone.now().strftime('%Y%m%d')
        NumberQuotationatthatday = get_next_quotation_number(today)
        QuotationNo = f"{today}-{NumberQuotationatthatday:04}"

        ExpiredDate = request.POST.get('expired_date', False)
        is_active = 1
        
        print("STATUS = ", Status)

        query = f'INSERT INTO Quotation VALUES ( null, \
                "{CustomerID}", \
                "{ProductID}", \
                "{ProductName}", \
                "{ProductVersion}", \
                "{Quantity}", \
                "{BudgetPerUnit}", \
                "{CostExcludeOperation}", \
                "{OperationCost}", \
                "{ManagementCostPercentage}", \
                "{MaterialCostNumber}", \
                "{MaterialCostPercentage}", \
                "{OutsourceCostNumber}", \
                "{OutsourceCostPercentage}", \
                "{OperationBudget}", \
                "{timezone.now()}", \
                "{Username}", \
                "{ Status,}", \
                "{is_active}", \
                "{QuotationNo}", \
                "{ExpiredDate}" )'
        # return HttpResponse(query)
        print(query)

        with connection.cursor() as cursor:
            cursor.execute(query)
        
        insertQuotationProcess(request)
        insertQuotationOther(request)
        insertQuotationMaterial(request)

        return redirect('/Quotation/')

def get_next_quotation_number(today):
    # Query the database to get the latest quotation number for the current day
    query = "SELECT MAX(CAST(SUBSTRING_INDEX(QUOTATION_NO, '-', -1) AS SIGNED)) FROM Quotation WHERE DATE(CREATED_AT) = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, [today])
        result = cursor.fetchone()
    
    if result and result[0]:
        return int(result[0]) + 1
    else:
        return 1

    
def detailQuotation(request, quotation_id):
    if request.user.is_authenticated:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        #detail quotation
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
        quotation['expired_date'] = str(quotation['expired_date'])
        # totalMaterialCost =  quotation["MATERIAL_COST_NUMBER"] * ( quotation["MATERIAL_COST_PERCENTAGE"] / 100 )
        # totalOutsourceCost = quotation["OUTSOURCE_COST_NUMBER"] * ( quotation["OUTSOURCE_COST_PERCENTAGE"] / 100 )
        
        #data customer
        query = "SELECT * FROM CUSTOMER"

        cursor.execute(query)
        customer = cursor.fetchall()
        customer_js = json.dumps(customer)

        #data part
        query = 'SELECT * FROM part'

        cursor.execute(query)
        part_reflect_cost = cursor.fetchall()
        part_reflect_cost_js = json.dumps(part_reflect_cost)

        #data other
        query = "SELECT * FROM OTHER"

        cursor.execute(query)
        other = cursor.fetchall()
        other_js = json.dumps(other)

        #data process
        query = "SELECT * FROM PROCESS"

        cursor.execute(query)
        process = cursor.fetchall()
        process_js = json.dumps(process)
  
        #detail quotation material
        query = 'SELECT * FROM quotation_material \
                LEFT JOIN PART ON PART.idPART = QUOTATION_MATERIAL.MATERIAL_ID \
                WHERE Quotation_ID = ' + str(quotation_id)
        
        cursor.execute(query)
        quotation_material = cursor.fetchall()
        quotation_material_js = json.dumps(quotation_material)
        print("quotation_MATERIAL ====> ", quotation_material_js)

        # detail quotation process
        query = 'select * from quotation_process \
                JOIN PROCESS ON QUOTATION_PROCESS.PROCESS_ID = PROCESS.ProcessID \
                where Quotation_ID = ' + str(quotation_id)
                
        cursor.execute(query)
        quotation_process = cursor.fetchall()
        quotation_process_js = json.dumps(quotation_process)
        # print("quotation process = ", quotation_process)

        # detail quotation other
        query = 'select * from quotation_other \
                    JOIN OTHER ON quotation_other.OTHER_ID = OTHER.OtherId \
                    where Quotation_ID =' + str(quotation_id)
        cursor.execute(query)
        quotation_other = cursor.fetchall()
        quotation_other_js = json.dumps(quotation_other)
        # print("quotation other = ", quotation_other)

        print("quotation = ", quotation)
        # context
        context = { 
            'q' : quotation,
            'quotation' : quotationjs,
            'TotalBudget' : totalBudget,
            'TotalCost' : totalCost,
            "ManagementCost" : managementCost,

            'other' : other,
            'other_js' : other_js,

            'process' : process,
            'process_js' : process_js,

            'customer' : customer,
            'customer_js' : customer_js,

            'partreflectcost' : part_reflect_cost,
		    'partreflectcostjs' : part_reflect_cost_js,

            'quotation_material' : quotation_material,
            'quotation_material_js' : quotation_material_js,

            'quotation_process' : quotation_process,
            'quotation_process_js' : quotation_process_js,

            'quotation_other' : quotation_other,
            'quotation_other_js' : quotation_other_js,
        }

    return render(request, 'editquotation.html', context)

def updateQuotationMaterial(request, quotation_id):
    # ========== Quotation Material ==========
    BoardArr = request.POST['BoardArr'].split(',')
    BarArr = request.POST['BarArr'].split(',')
    print("-- BOARDARR inside Update = ", BoardArr )
    QUOTATION_ID = getLastCreatedQuotationID()

    MaterialList = request.POST.getlist('material_id')
    MaterialLength = len(MaterialList)
    if(MaterialLength == 0) : return

    print(MaterialLength)
    USED_QUANTITY = request.POST.getlist('usedQuantity')
    BoardArrView = [BoardArr[i:i+29] for i in range(0, len(BoardArr), 29)]
    BarArrView = [BarArr[i:i+27] for i in range(0, len(BarArr), 29)]
    for item in BoardArrView:
        print("BOARDARR Update = ", item )
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
        query =  f'UPDATE quotation_material SET \
            MATERIAL_ID = { MaterialID }, \
            USED_QUANTITY = { UsedQuantity }, \
            BOARD_VERTICAL_SCALE = { BoardVerticalScale }, \
            BOARD_HORIZONTAL_SCALE = { BoardHorizontalScale }, \
            BOARD_THICKNESS = { BoardThickness }, \
            BOARD_VERTICAL_SCALE_FROM_NUMBER = { BoardVerticalScaleFromNumber }, \
            BOARD_HORIZONTAL_SCALE_FROM_NUMBER = { BoardHorizontalScaleFromNumber }, \
            BOARD_EXPOSED_FROM_NUMBER = { BoardExposedFromNumber }, \
            BOARD_MARGIN_FROM_NUMBER = { BoardMarginFromNumber }, \
            BOARD_MATERIAL_COST_FROM_NUMBER = { BoardMaterialCostFromNumber }, \
            BOARD_EXPOSED_FROM_PART_SCALE = { BoardExposedFromPartScale }, \
            BOARD_MARGIN_FROM_PART_SCALE = { BoardMarginFromPartScale }, \
            BAR_PART_SCALP = { BarPartScalp }, \
            BAR_DIAMETER = { BarDiameter }, \
            BAR_EXPOSED = { BarExposed }, \
            BAR_LENGTH = { BarLength }, \
            BAR_EDGE_LOSS = { BarEdgeLoss }, \
            BAR_KEFT_LOSS = { BarKeftLoss } \
            WHERE QUOTATION_ID = {quotation_id} AND MATERIAL_ID = {MaterialID}'
        
        print( "-- Update Material Query = ", query )
        with connection.cursor() as cursor:
            cursor.execute(query)
   

    # ========== Update Quotation Other ==========
def updateQuotationOther(request, quotation_id):
    OtherId = request.POST.getlist('othersId')
    OtherLength = len(OtherId)
    OtherPrice = request.POST.getlist('otherprice')
    OtherPercentage = request.POST.getlist('otherpercentage')

    #save is_per_unit status
    perUnit_Arr = []
    for i in range(0, OtherLength):
        OtherIsPerUnit = request.POST.get(f'otherisperunit-{i+1}', False)
       
        if OtherIsPerUnit == "on":
            perUnit_Arr.append(1)
        else:
            perUnit_Arr.append(0)

    #untuk ngambil semua other id dari db
    query = f'select OTHER_ID from quotation_other where QUOTATION_ID = {quotation_id}'
    with connection.cursor() as cursor:
        cursor.execute(query)
        other_id_list_from_db = cursor.fetchall()

        #save  all OTHER_ID ONLY from db from this quotation in list
        #before : ( (5,), (6, ) )
        #after : [5, 6]
        other_id_list_from_db = [i[0] for i in other_id_list_from_db]
  
    for i in range(0, len(other_id_list_from_db)):
        if(not(str(other_id_list_from_db[i]) in OtherId)):
            #remove yang ada di db tapi gaada di quotation
            #Remove other list that exist in database but deleted in edited quotation
            query = f'DELETE FROM quotation_other WHERE QUOTATION_ID = "{quotation_id}" AND OTHER_ID = "{other_id_list_from_db[i]}"'
            with connection.cursor() as cursor:
                cursor.execute(query)

    # print("OTHER ID SISA = ", OtherId)
    # print("OTHER PRICE SISA = ", OtherPrice)
    # print("OTHER PERCENTAGE SISA = ", OtherPercentage)
    # print("OTHER IS PER UNIT SISA = ", OtherIsPerUnit)

    for i in range(0, OtherLength):
        #check if current index of other list is exist in the database
        #if exist it will update
        #if not exist it will insert new
        query = f'select exists (select * from quotation_other where QUOTATION_ID = {quotation_id} and OTHER_ID = {OtherId[i]}) as a;'
        with connection.cursor() as cursor:
            cursor.execute(query)
            res = cursor.fetchall()
        # print("RES ADA GA OTHER  = ", res[0][0])

        if(res[0][0] == 1):
            query = f'UPDATE quotation_other \
                SET \
                OTHER_ID = "{OtherId[i]}", \
                OTHER_PRICE =  "{OtherPrice[i]}", \
                OTHER_PERCENTAGE =  "{OtherPercentage[i]}", \
                OTHER_IS_PER_UNIT =  "{perUnit_Arr[i]}" \
                WHERE QUOTATION_ID = "{quotation_id}" AND OTHER_ID = "{OtherId[i]}"'
        elif(res[0][0] == 0):
            query = f'INSERT INTO quotation_other VALUES (null, "{quotation_id}", "{OtherId[i]}", "{OtherPrice[i]}", "{OtherPercentage[i]}", "{perUnit_Arr[i]}")'
   
    
      


        print("Update Other Query = ", query)
        with connection.cursor() as cursor:
            cursor.execute(query)

   

# ========== Update Quotation Process ==========
def updateQuotationProcess(request, quotation_id):
    ProcessId = request.POST.getlist('ProcessId')
    ProcessLength = len(ProcessId)
    Opesum = request.POST.getlist('opeSum')
    OpePerOpeBudgetRatio = request.POST.getlist('operationPerOperationBudgetRatio')
    OpePerBudgetRatio = request.POST.getlist('operationPerBudgetRatio')
    SetTime = request.POST.getlist('setTime')
    OpeTime = request.POST.getlist('opeTime')
    TotalOpeTime = request.POST.getlist('totalOpeTime')
    QuantityPerMin = request.POST.getlist('quantityPerMinute')

    #untuk ngambil semua other id dari db
    query = f'select PROCESS_ID from quotation_process where QUOTATION_ID = {quotation_id}'
    with connection.cursor() as cursor:
        cursor.execute(query)
        process_id_list_from_db = cursor.fetchall()

        #save  all OTHER_ID ONLY from db from this quotation in list
        #before : ( (5,), (6, ) )
        #after : [5, 6]
        process_id_list_from_db = [i[0] for i in process_id_list_from_db]
  
    for i in range(0, len(process_id_list_from_db)):
        print("ASFASFASFSAF = ", str(process_id_list_from_db[i]), ProcessId)
        if( not(str(process_id_list_from_db[i]) in ProcessId)):
            query = f'DELETE FROM quotation_process WHERE QUOTATION_ID = "{quotation_id}" AND PROCESS_ID = "{process_id_list_from_db[i]}"'
            with connection.cursor() as cursor:
                cursor.execute(query)

    print("PROCESS ID SISA = ", ProcessId)
    print("PROCESS OPESUM SISA = ", Opesum)
    print("PROCESS SETTIME SISA = ", SetTime)
    print("PROCESS OPETIME SISA = ", OpeTime)

    for i in range(0, ProcessLength):
        #check if current index of other list is exist in the database
        #if exist it will update
        #if not exist it will insert new
        query = f'select exists (select * from quotation_process where QUOTATION_ID = {quotation_id} and PROCESS_ID = {ProcessId[i]}) as a;'
        with connection.cursor() as cursor:
            cursor.execute(query)
            res = cursor.fetchall()
        if(res[0][0] == 1):
            query = f'UPDATE quotation_process \
                SET \
                PROCESS_ID = "{ProcessId[i]}", \
                OPESUM =  "{Opesum[i]}", \
                OPE_PER_OPE_BUDGET_RATIO =  "{OpePerOpeBudgetRatio[i]}", \
                OPE_PER_BUDGET_RATIO =  "{OpePerBudgetRatio [i]}", \
                SETTIME =  "{SetTime [i]}", \
                OPETIME =  "{OpeTime[i]}", \
                TOTAL_OPETIME =  "{TotalOpeTime[i]}", \
                QUANTITY_PER_MIN =  "{QuantityPerMin[i]}" \
                WHERE QUOTATION_ID = "{quotation_id}" AND PROCESS_ID = "{ProcessId[i]}"'
        elif(res[0][0] == 0):
            query = 'INSERT INTO quotation_process VALUES (null, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
                quotation_id,
                ProcessId[i],
                Opesum[i],
                OpePerOpeBudgetRatio[i],
                OpePerBudgetRatio[i],
                SetTime[i],
                OpeTime[i],
                TotalOpeTime[i],
                QuantityPerMin[i],
            )
        
        print("Update Process Query = ", query)
        with connection.cursor() as cursor:
            cursor.execute(query)

def updateQuotation(request, quotation_id):
    # return HttpResponse('asdasf')
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
        ExpiredDate = request.POST.get('expired_date', False)
        
        is_active = 1
        print("STATUS = ", Status)

        query = f'UPDATE Quotation \
            SET PRODUCT_ID = "{ ProductID }", \
                PRODUCT_NAME = "{ ProductName }", \
                PRODUCT_VERSION = "{ ProductVersion }", \
                QUANTITY = "{ Quantity }", \
                BUDGET_PER_UNIT = "{ BudgetPerUnit }", \
                COST_EXCLUDE_OPERATION = "{  CostExcludeOperation }", \
                OPERATION_COST = "{ OperationCost }", \
                MANAGEMENT_COST_PERCENTAGE = "{ ManagementCostPercentage }", \
                MATERIAL_COST_NUMBER = "{ MaterialCostNumber }", \
                MATERIAL_COST_PERCENTAGE = "{ MaterialCostPercentage }", \
                OUTSOURCE_COST_NUMBER = "{ OutsourceCostNumber }", \
                OUTSOURCE_COST_PERCENTAGE = "{ OutsourceCostPercentage }", \
                OPERATION_BUDGET = "{ OperationBudget }", \
                CREATED_AT = "{  timezone.now() }", \
                ACTIVITY_LOG = "{ Username }", \
                QUOTATION_STATUS = "{ Status }", \
                expired_date = "{ExpiredDate }", \
                is_active = {is_active} \
                WHERE QUOTATION_ID = { quotation_id }'
        
        print( "UPDATE QUERY = ", query)
        with connection.cursor() as cursor:     
            cursor.execute(query)
            
        updateQuotationOther(request, quotation_id)
        updateQuotationMaterial(request, quotation_id)
        updateQuotationProcess(request, quotation_id)

        return redirect('/Quotation/')
    

def copyQuotation(request,  quotation_id):

    today = timezone.now().strftime('%Y%m%d')
    NumberQuotationatthatday = get_next_quotation_number(today)
    QuotationNo = f"{today}-{NumberQuotationatthatday:04}"
    print('-- QUOTATION_NO = ', QuotationNo)
    query = f"INSERT INTO QUOTATION ( \
            SELECT  \
            null, \
            CUSTOMER_ID, \
            PRODUCT_ID, \
            PRODUCT_NAME, \
            PRODUCT_VERSION, \
            QUANTITY, \
            BUDGET_PER_UNIT, \
            COST_EXCLUDE_OPERATION, \
            OPERATION_COST, \
            MANAGEMENT_COST_PERCENTAGE, \
            MATERIAL_COST_NUMBER, \
            MATERIAL_COST_PERCENTAGE, \
            OUTSOURCE_COST_NUMBER, \
            OUTSOURCE_COST_PERCENTAGE, \
            OPERATION_BUDGET, \
            CREATED_AT, \
            ACTIVITY_LOG, \
            QUOTATION_STATUS, \
            is_active, \
            '{QuotationNo}', \
            EXPIRED_DATE \
            FROM quotation \
            WHERE QUOTATION_ID = {quotation_id});"
    print("-- query copy quotaion = ", query)
    with connection.cursor() as cursor:
        cursor.execute(query)
        q = cursor.fetchall()
        
    return redirect('/Quotation/')
    return HttpResponse(q)

