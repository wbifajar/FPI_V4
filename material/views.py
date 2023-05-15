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

def InsertForm(request):
    nama = request.POST['nama']
    price = request.POST['price']
    with connection.cursor() as cursor:
        query = 'Insert Into Material values (null, "{}", {})'.format(nama, price)
        cursor.execute( query )
    return redirect('/material')