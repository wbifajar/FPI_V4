from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


from django.db import connection
from .databaseConnect import *
# Create your views here.

def index(request):

    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM AUTH_USER'
    cursor.execute( query )
    res = cursor.fetchall()

    context = {
        'auth_user' : res, 
    }

    return render(request, 'user_index.html', context)

def insert(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            return redirect( '/', user)
        else:
            return render(request, 'user_insert.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'user_insert.html', {'form': form})


    return render(request, 'user_insert.html')

def store(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            return redirect( '/', user)
        else:
            return render(request, 'user_insert.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'user_insert.html', {'form': form})

