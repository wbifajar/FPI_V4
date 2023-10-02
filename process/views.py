from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.db import connection
from .databaseConnect import *
# Create your views here.

def index(request):

    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM PROCESS'
    cursor.execute( query )
    res = cursor.fetchall()

    context = {
        'process' : res, 
    }

    return render(request, 'process_index.html', context)

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
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    SettingCost = request.POST.get('')

    query = f'UPDATE PROCESS SET \
                SettingCost = null, {1})'