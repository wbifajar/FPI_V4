from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
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

    return render(request, 'part_index.html', context)

def insert(request):
    return render(request, 'part_insert.html')

def store(request):
    PartName = request.POST.get('name', False)
    SpecificGravity = request.POST.get('spesificGravity', False)
    PartPrice = request.POST.get('price', False)
    query = f'INSERT INTO PART VALUES(null, "{PartName}", "{SpecificGravity}", "{PartPrice}")'
    query = f'INSERT INTO PART VALUES(null, "{PartName}", "{SpecificGravity}", "{PartPrice}")'

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
        'part' : res[0], 
        'part' : res[0], 
    }

    return render(request, 'part_edit.html', context)
    return render(request, 'part_edit.html', context)

def update(request, idPart):
    PartName = request.POST.get('name', False)
    SpecificGravity = request.POST.get('spesificGravity', False)
    PartPrice = request.POST.get('price', False)
    query = f'UPDATE PART \
        SET \
        name = "{PartName}", \
        spesificGravity = "{SpecificGravity}", \
        price = "{PartPrice}" \
        WHERE idPart = "{idPart}"'
    print(query)

    with connection.cursor() as cursor:
        cursor.execute(query)
    return redirect('/part')

def delete(request, idPart):
    query = f'DELETE FROM PART WHERE idPart = {idPart}'
    with connection.cursor() as cursor:
        cursor.execute(query)

    messages.add_message(request, messages.SUCCESS, "Part Deleted Sucessfuly")
    return redirect('/part')
    return redirect('/part')