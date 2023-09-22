from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from django.db import connection
from .databaseConnect import *
# Create your views here.

def index(request):
    connection = connect()
    cursor = connection.cursor(dictionary=True)
    query = "Select * from material"
    cursor.execute(query)
    materials = cursor.fetchall()

    context = {
        'Materials' : materials
    }

    print(materials)
    template = loader.get_template('material_index.html')

    return HttpResponse(template.render(context, request))

def insert(request):
    return render(request, "material_insert.html")

def store(request):
    nama = request.POST['name']
    price = request.POST['price']
    with connection.cursor() as cursor:
        query = f'Insert Into Material values (null, "{nama}", "{price}")'
        cursor.execute( query )
    return redirect('/material')

def edit(request, material_id):
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM MATERIAL WHERE idMaterial = ' + str(material_id)
    cursor.execute( query )
    res = cursor.fetchone()
    print( "ASFASDFSAFAS = ", res)
    context = {
        'material' : res, 
    }

    return render(request, 'edit.html', context)

def update(request, material_id):
    MaterialName = request.POST.get('name', False)
    MaterialPrice = request.POST.get('price', False)
    query = f'UPDATE MATERIAL \
        SET \
        Name = "{MaterialName}", \
        Price = "{MaterialPrice}" \
        WHERE idMaterial = "{material_id}"'
    print(query)

    with connection.cursor() as cursor:
        cursor.execute(query)
    return redirect('/material')

def delete(request, material_id):
    query = f'DELETE FROM MATERIAL WHERE idMaterial = {material_id}'
    with connection.cursor() as cursor:
        cursor.execute(query)

    return redirect('/material')