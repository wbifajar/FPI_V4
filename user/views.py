from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required
import bcrypt
from django.db import connection
from .databaseConnect import *
# Create your views here.

@permission_required('user.view_user', raise_exception=True)
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

@permission_required('user.change_user', raise_exception=True)
def edit(request, id):
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    user_query = 'SELECT AUTH_USER.id AS id, AUTH_USER.username, AUTH_USER.first_name, AUTH_USER.last_name, AUTH_USER.email, AUTH_USER.is_active, \
            AUTH_GROUP.name FROM AUTH_USER LEFT JOIN AUTH_USER_GROUPS ON AUTH_USER.id = AUTH_USER_GROUPS.user_id \
            LEFT JOIN AUTH_GROUP ON AUTH_GROUP.id = AUTH_USER_GROUPS.group_id WHERE AUTH_USER.ID = ' + str(id)
    
    group_query = 'SELECT AUTH_GROUP.id AS id, AUTH_GROUP.name FROM AUTH_GROUP'
    
    cursor.execute(user_query)
    res = cursor.fetchall()

    cursor.execute(group_query)
    groups = cursor.fetchall()

    context = {
        'user': res[0],
        'groups': groups,
    }

    return render(request, 'user_edit.html', context)


def update(request, id):
    # Get user data from request
    username = request.POST.get('username', '')
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    email = request.POST.get('email', '')
    is_active = request.POST.get('is_active', False)
    group_ids = request.POST.getlist('userGroup')  # Adjusted to match the name attribute in the HTML form

    # Update user information using parameterized query
    user_query = 'UPDATE AUTH_USER SET ' \
                 'username = %s, ' \
                 'first_name = %s, ' \
                 'last_name = %s, ' \
                 'email = %s, ' \
                 'is_active = %s ' \
                 'WHERE ID = %s'

    # Update user's group memberships - delete existing and insert new
    delete_group_query = 'DELETE FROM AUTH_USER_GROUPS WHERE user_id = %s'
    insert_group_query = 'INSERT INTO AUTH_USER_GROUPS (user_id, group_id) VALUES (%s, %s)'

    with connection.cursor() as cursor:
        cursor.execute(user_query, [username, first_name, last_name, email, is_active, id])
        cursor.execute(delete_group_query, [id])

        for group_id in group_ids:
            cursor.execute(insert_group_query, [id, group_id])

    return redirect('/user')
