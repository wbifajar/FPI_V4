from django.shortcuts import render, redirect

import sys
sys.path.append("..")
from django.db import connection
from .databaseConnect import *

# Create your views here.
def index(request):
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM managementmaster'
    cursor.execute( query )
    managementmaster = cursor.fetchall()


    context = {
        'managementmaster' : managementmaster[0], 
    }
    return render(request, 'managementmaster.html', context)

def edit(request):
    coName = request.POST.get('coName', False)
    bankAccName = request.POST.get('bankAccName', False)
    bankName = request.POST.get('bankName', False)
    accNumber = request.POST.get('accNumber', False)
    bankBranch = request.POST.get('bankBranch', False)
    bankAddress = request.POST.get('bankAddress', False)
    query = f'UPDATE managementmaster \
        SET \
        co_name = "{coName}", \
        bankAccountName = "{bankAccName}", \
        bankName = "{bankName}", \
        accountNumber = "{accNumber}", \
        bankBranch = "{bankBranch}", \
        bankAddress = "{bankAddress}" \
        WHERE id_managementMaster = 1'
    print(query)

    with connection.cursor() as cursor:
        cursor.execute(query)
    return redirect('/managementmaster')

#   return render(request, 'settingquotation.html')   

