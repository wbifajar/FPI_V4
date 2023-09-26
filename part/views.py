from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.db import connection
from .databaseConnect import *
# Create your views here.

def index(request):

    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM PART'
    cursor.execute( query )
    res = cursor.fetchall()

    context = {
        'part' : res, 
    }

    return render(request, 'index.html', context)
    return HttpResponse(res)

def insert(request):
    return render(request, 'insert.html')

def store(request):
    PartName = request.POST.get('name', False)
    SpecificGravity = request.POST.get('spesificGravity', False)
    PartPrice = request.POST.get('price', False)
    query = f'INSERT INTO EMPLOYEE VALUES(null, "{PartName}", "{SpecificGravity}", "{PartPrice}")'

    with connection.cursor() as cursor:
        cursor.execute(query)
    print("QUERY = ", query)
    return redirect('/part')

def edit(request, idPart):
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM PART WHERE IDPART = ' + str(idPart)
    cursor.execute( query )
    res = cursor.fetchall()

    context = {
        'employee' : res[0], 
    }

    return render(request, 'edit.html', context)

def update(request, idPart):
    PartName = request.POST.get('name', False)
    SpecificGravity = request.POST.get('spesificGravity', False)
    PartPrice = request.POST.get('price', False)
    query = f'UPDATE EMPLOYEE \
        SET \
        NAME = "{PartName}", \
        SPESIFICGRAVITY = "{SpecificGravity}", \
        PRICE = "{PartPrice}", \
        WHERE idPart = "{idPart}"'
    print(query)

    with connection.cursor() as cursor:
        cursor.execute(query)
    return redirect('/part')

def delete(request, idPart):
    query = f'DELETE FROM EMPLOYEE WHERE idPart = {idPart}'
    with connection.cursor() as cursor:
        cursor.execute(query)

    return redirect('/part')