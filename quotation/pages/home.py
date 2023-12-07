from django.shortcuts import render

import sys
sys.path.append("..")

from ..databaseConnect import *


def home(request):
    connection = connect()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('select * from pin')
    data = cursor.fetchall() 
    # print(data)

    if request.method == "POST":
        workinput = request.POST.get('workinput')
        parts = request.POST.get('parts')
        inorder = request.POST.get('inorder')
        material1 = request.POST.get('material1')
        outorder = request.POST.get('outorder')
        factory = request.POST.get('factory')
        office = request.POST.get('office')
        depositpayment = request.POST.get('depositpayment')
        van = request.POST.get('van')
        quotation = request.POST.get('Quotation')
        mastermaintenance = request.POST.get('mastermaintenance')
        sysenvironment = request.POST.get('sysenvironment')
        button = request.POST.get('button')

        
        button = button.split('-')

        if button[0] == 'workinput' :
            cursor.execute(f'insert into pin values (null,"{workinput}")')
            connection.commit()
        if button[0] == 'parts' :
            cursor.execute(f'insert into pin values (null,"{parts}")')
            connection.commit()
        if button[0] == 'inorder' :
            cursor.execute(f'insert into pin values (null,"{inorder}")')
            connection.commit()
        if button[0] == 'material1' :
            cursor.execute(f'insert into pin values (null,"{material1}")')
            connection.commit()
        if button[0] == 'outorder' :
            cursor.execute(f'insert into pin values (null,"{outorder}")')
            connection.commit()
        if button[0] == 'factory' :
            cursor.execute(f'insert into pin values (null,"{factory}")')
            connection.commit()
        if button[0] == 'office' :
            cursor.execute(f'insert into pin values (null,"{office}")')
            connection.commit()
        if button[0] == 'depositpayment' :
            cursor.execute(f'insert into pin values (null,"{depositpayment}")')
            connection.commit()
        if button[0] == 'van' :
            cursor.execute(f'insert into pin values (null,"{van}")')
            connection.commit()
        if button[0] == 'Quotation' :
            cursor.execute(f'insert into pin values (null,"{quotation}")')
            connection.commit()
        if button[0] == 'mastermaintenance' :
            cursor.execute(f'insert into pin values (null,"{mastermaintenance}")')
            connection.commit()
        if button[0] == 'sysenvironment' :
            cursor.execute(f'insert into pin values (null,"{sysenvironment}")')
            connection.commit()
        elif button[0] == 'deletelist':
            cursor.execute(f'DELETE FROM pin WHERE idPin = {button[1]}')
            connection.commit()
        cursor.execute('select * from pin')
        data = cursor.fetchall() 
        
    context = {
        'data' : data   
    }

    return render(request, 'home.html', context)