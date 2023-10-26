from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


from django.db import connection
from .databaseConnect import *
# Create your views here.

def index(request):

    connection = connect()
    cursor = connection.cursor(dictionary=True)

    # query = 'SELECT AUTH_USER.id AS user_id, AUTH_GROUP.id AS group_id FROM AUTH_USER LEFT JOIN AUTH_USER_GROUPS ON AUTH_USER.id = AUTH_USER_GROUPS.user_id LEFT JOIN AUTH_GROUP ON AUTH_GROUP.id = AUTH_USER_GROUPS.group_id UNION SELECT * FROM AUTH_USER LEFT JOIN AUTH_USER_GROUPS ON AUTH_USER.id = AUTH_USER_GROUPS.user_id LEFT JOIN AUTH_GROUP ON AUTH_GROUP.id = AUTH_USER_GROUPS.group_id'
    query = 'SELECT AUTH_USER.id AS id, AUTH_USER.username, AUTH_USER.date_joined, AUTH_GROUP.name \
            from AUTH_USER \
            LEFT JOIN AUTH_USER_GROUPS ON AUTH_USER.id = AUTH_USER_GROUPS.user_id \
            LEFT JOIN AUTH_GROUP ON AUTH_GROUP.id = AUTH_USER_GROUPS.group_id'
    
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

