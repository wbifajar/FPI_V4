from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.db import connection
from .databaseConnect import *
# Create your views here.
@permission_required('process.view_process', raise_exception=True)
def index(request):
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM PROCESS'
    cursor.execute( query )
    res = cursor.fetchall()

    query = 'SELECT * FROM category_process'
    cursor.execute( query )
    category_process = cursor.fetchall()

    context = {
        'process' : res, 
        'category' : category_process,
    }

    return render(request, 'process_index.html', context)

@permission_required('process.add_process', raise_exception=True)
def insert(request):
    query_category = 'SELECT * FROM category_process'
    with connection.cursor() as cursor:
        cursor.execute(query_category)
        category_process = cursor.fetchall()

    context = {
        'category': category_process,
    }
    print(category_process)
    return render(request, 'process_insert.html', context)

def store(request):
    ProcessName = request.POST.get('name')
    SettingCost = request.POST.get('setting_cost')
    ProcessCost = request.POST.get('process_cost')
    DefaultSetTime = request.POST.get('default_set_time')
    DefaultOpeTime = request.POST.get('default_ope_time')
    idCategory = request.POST.get('idCategory')

    query = f"INSERT INTO PROCESS VALUES(\
                null, \
                '{ProcessName}', \
                '{SettingCost}', \
                '{ProcessCost}', \
                '{DefaultSetTime}', \
                '{DefaultOpeTime}', \
                '{idCategory}')"
    
    with connection.cursor() as cursor:
        cursor.execute(query)

    return redirect('/process')

@permission_required('process.change_process', raise_exception=True)
def edit(request, process_id):

    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query_process= 'SELECT process.*, category_process.categoryName FROM process LEFT JOIN category_process ON process.CategoryId = category_process.idCategory WHERE process.ProcessId = ' + str(process_id)
    cursor.execute(query_process)
    proc = cursor.fetchall()

    query_category = '''
        SELECT category_process.*
        FROM category_process
        WHERE category_process.idCategory NOT IN (
            SELECT process.CategoryId
            FROM process
            WHERE process.ProcessId = %s
        )
    '''
    cursor.execute(query_category, [process_id])
    procOption = cursor.fetchall()
    # print(procOption)

    context = {
        "process" : proc[0],
        "procOption" : procOption,
    }

    return render(request, 'process_edit.html', context)

def update(request, process_id):
    ProcessName = request.POST.get('name')
    SettingCost = request.POST.get('setting_cost')
    ProcessCost = request.POST.get('process_cost')
    DefaultSetTime = request.POST.get('default_set_time')
    DefaultOpeTime = request.POST.get('default_ope_time')
    idCategory = request.POST.get('idCategory')
    # print(idCategory)

    query = f'UPDATE PROCESS SET \
                Name = "{ProcessName}", \
                SettingCost = "{SettingCost}", \
                ProcessCost = "{ProcessCost}", \
                DefaultSetTime = "{DefaultSetTime}", \
                DefaultOpeTime = "{DefaultOpeTime}", \
                CategoryId = "{idCategory}" \
                WHERE ProcessId = {process_id} '

    with connection.cursor() as cursor:
        cursor.execute(query)
    return redirect('/process')

@permission_required('process.delete_process', raise_exception=True)
def delete(request, process_id):
    query = f"DELETE FROM PROCESS WHERE ProcessId = {process_id}"

    with connection.cursor() as cursor:
        cursor.execute(query)
    
    return redirect('/process')


def insertCategory(request):
    return render(request, 'category_insert.html')

def storeCategory(request):
    categoryName = request.POST.get('categoryName')

    query = f"INSERT INTO category_process VALUES(\
                null, \
                '{categoryName}')"

    with connection.cursor() as cursor:
        cursor.execute(query)
    return redirect('/process')

def editCategory(request, category_id):

    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM category_process WHERE idCategory = ' + str(category_id)
    cursor.execute(query)

    category = cursor.fetchall()

    context = {
        "category" : category[0]
    }

    return render(request, 'category_edit.html', context)

def updateCategory(request, category_id):

    categoryName = request.POST.get('categoryName')

    query = f'UPDATE category_process SET categoryName = "{categoryName}" WHERE idCategory = {category_id} '

    with connection.cursor() as cursor:
        cursor.execute(query)
    return redirect('/process')