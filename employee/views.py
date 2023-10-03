from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.db import connection
from .databaseConnect import *
# Create your views here.

def index(request):

    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM EMPLOYEE'
    cursor.execute( query )
    res = cursor.fetchall()

    context = {
        'employees' : res, 
    }

    return render(request, 'employee_index.html', context)
    return HttpResponse(res)

def insert(request):
    return render(request, 'insert.html')

def store(request):
    EmployeeName = request.POST.get('name', False)
    EmployeeAddress = request.POST.get('address', False)
    EmployeeSection = request.POST.get('section', False)
    EmployeePhone = request.POST.get('phone-number', False)
    EmployeeStatus = request.POST.get('status', False)
    query = f'INSERT INTO EMPLOYEE VALUES(null, "{EmployeeName}", "{EmployeeAddress}", "{EmployeeSection}", "{EmployeePhone}", "{EmployeeStatus}")'

    with connection.cursor() as cursor:
        cursor.execute(query)
    print("QUERY = ", query)
    return redirect('/employee')

def edit(request, employee_id):
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM EMPLOYEE WHERE EMPLOYEE_ID = ' + str(employee_id)
    cursor.execute( query )
    res = cursor.fetchall()

    context = {
        'employee' : res[0], 
    }

    return render(request, 'employee_edit.html', context)

def update(request, employee_id):
    EmployeeName = request.POST.get('name', False)
    EmployeeAddress = request.POST.get('address', False)
    EmployeeSection = request.POST.get('section', False)
    EmployeePhone = request.POST.get('phone-number', False)
    EmployeeStatus = request.POST.get('status', False)
    query = f'UPDATE EMPLOYEE \
        SET \
        EMPLOYEE_NAME = "{EmployeeName}", \
        EMPLOYEE_ADDRESS = "{EmployeeAddress}", \
        EMPLOYEE_SECTION = "{EmployeeSection}", \
        EMPLOYEE_PHONE = "{EmployeePhone}", \
        EMPLOYEE_STATUS = "{EmployeeStatus}" \
        WHERE EMPLOYEE_ID = "{employee_id}"'
    print(query)

    with connection.cursor() as cursor:
        cursor.execute(query)
    return redirect('/employee')

def delete(request, employee_id):
    query = f'DELETE FROM EMPLOYEE WHERE EMPLOYEE_ID = {employee_id}'
    with connection.cursor() as cursor:
        cursor.execute(query)

    return redirect('/employee')

