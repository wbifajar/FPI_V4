from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.db import connection
from .databaseConnect import *
# Create your views here.

def index(request):

    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM OTHER'
    cursor.execute( query )
    res = cursor.fetchall()

    context = {
        'other' : res, 
    }

    return render(request, 'other_index.html', context)
    return HttpResponse(res)

def insert(request):
    return render(request, 'other_insert.html')

def store(request):
    otherName = request.POST.get('name', False)
    query = f'INSERT INTO other VALUES(null, "{otherName}")'

    with connection.cursor() as cursor:
        cursor.execute(query)
    print("QUERY = ", query)
    return redirect('/other')

def edit(request, OtherId):
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM OTHER WHERE OtherId = ' + str(OtherId)
    cursor.execute( query )
    res = cursor.fetchall()

    context = {
        'other' : res[0], 
    }

    return render(request, 'other_edit.html', context)

def update(request, OtherId):
    OtherName = request.POST.get('Name', False)
    query = f'UPDATE OTHER\
        SET \
        Name = "{OtherName}", \
        WHERE OtherId = "{OtherId}"'
    print(query)

    with connection.cursor() as cursor:
        cursor.execute(query)
    return redirect('/other')

def delete(request, OtherId):
    query = f'DELETE FROM OTHER WHERE OtherId = {OtherId}'
    with connection.cursor() as cursor:
        cursor.execute(query)

    return redirect('/other')