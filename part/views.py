from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.db import connection
from .databaseConnect import *
# Create your views here.
@permission_required('material.view_material', raise_exception=True)
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

@permission_required('material.add_material', raise_exception=True)
def store(request):
    PartName = request.POST.get('name', False)
    SpecificGravity = request.POST.get('spesificGravity', False)
    PartPrice = request.POST.get('price', False)
    PartStatus = request.POST.get('partStatus', False)
    query = f'INSERT INTO PART VALUES(null, "{PartName}", "{SpecificGravity}", "{PartPrice}", "{PartStatus}")'

    with connection.cursor() as cursor:
        cursor.execute(query)
    print("QUERY = ", query)

    return redirect('/part')

@permission_required('material.change_material', raise_exception=True)
def edit(request, idPart):
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM PART WHERE IDPART = ' + str(idPart)
    cursor.execute( query )
    res = cursor.fetchall()

    context = {
        'part' : res[0], 
    }

    return render(request, 'part_edit.html', context)

def update(request, idPart):
    PartName = request.POST.get('name', False)
    SpecificGravity = request.POST.get('spesificGravity', False)
    PartPrice = request.POST.get('price', False)
    PartStatus = request.POST.get('partStatus', False)
    query = f'UPDATE PART \
        SET \
        name = "{PartName}", \
        spesificGravity = "{SpecificGravity}", \
        price = "{PartPrice}", \
        statusPart = "{PartStatus}" \
        WHERE idPart = "{idPart}"'
    print(query)

    with connection.cursor() as cursor:
        cursor.execute(query)
    return redirect('/part')

@permission_required('material.delete_material', raise_exception=True)
def delete(request, idPart):
    query = f'DELETE FROM PART WHERE idPart = {idPart}'
    with connection.cursor() as cursor:
        cursor.execute(query)

    messages.add_message(request, messages.SUCCESS, "Part Deleted Sucessfuly")
    return redirect('/part')