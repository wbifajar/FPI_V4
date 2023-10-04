from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.db import connection
from .databaseConnect import *
# Create your views here.

def index(request):
    ignore_this_variable = 1
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM PROCESS'
    cursor.execute( query )
    res = cursor.fetchall()

    context = {
        'process' : res, 
    }

    return render(request, 'process_index.html', context)

def insert(request):
    return render(request, 'process_insert.html')

def store(request):
    
    ProcessName = request.POST.get('name')
    SettingCost = request.POST.get('setting_cost')
    ProcessCost = request.POST.get('process_cost')
    DefaultSetTime = request.POST.get('default_set_time')
    DefaultOpeTime = request.POST.get('default_ope_time')

    query = f"INSERT INTO PROCESS VALUES(\
                null, \
                '{ProcessName}', \
                '{SettingCost}', \
                '{ProcessCost}', \
                '{DefaultSetTime}', \
                '{DefaultOpeTime}')"
    
    with connection.cursor() as cursor:
        cursor.execute(query)
    return redirect('/process')

def edit(request, process_id):

    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM PROCESS WHERE ProcessId = ' + str(process_id)
    cursor.execute(query)

    proc = cursor.fetchall()

    context = {
        "process" : proc[0]
    }

    return render(request, 'process_edit.html', context)

def update(request, process_id):

    ProcessName = request.POST.get('name')
    SettingCost = request.POST.get('setting_cost')
    ProcessCost = request.POST.get('process_cost')
    DefaultSetTime = request.POST.get('default_set_time')
    DefaultOpeTime = request.POST.get('default_ope_time')

    query = f'UPDATE PROCESS SET \
                SettingCost = "{SettingCost}", \
                ProcessCost = "{ProcessCost}", \
                DefaultSetTime = "{DefaultSetTime}", \
                DefaultOpeTime = "{DefaultOpeTime}" \
                WHERE ProcessId = {process_id} '

    with connection.cursor() as cursor:
        cursor.execute(query)
    return redirect('/process')

def delete(request, process_id):
    query = f"DELETE FROM PROCESS WHERE ProcessId = {process_id}"

    with connection.cursor() as cursor:
        cursor.execute(query)
    return redirect('/process')