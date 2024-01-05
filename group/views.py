from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import connection
from .databaseConnect import *
import json

# Create your views here.
@permission_required('group.view_group', raise_exception=True)
def index(request):
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM auth_group'
    cursor.execute( query )
    groups = cursor.fetchall()


    context = {
        'groups' : groups, 
    }
    return render(request, 'group_index.html', context)


def group_permission(request, group_id):
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT permission_id FROM auth_group_permissions where group_id = ' + str(group_id)
    cursor.execute( query )
    group_permissions = cursor.fetchall()
    group_permissions_js = json.dumps(group_permissions)

    query = 'SELECT * FROM auth_permission'
    cursor.execute( query )
    permission = cursor.fetchall()

    query = 'SELECT * FROM auth_group where id = ' + str(group_id)
    cursor.execute( query )
    group = cursor.fetchall()

    context = {
        'group_permissions' : group_permissions, 
        'group_permissions_js' : group_permissions_js, 
        
        'group' : group[0],

        'permissions' : permission,
    }
    return render(request, 'group_permission.html', context)

@permission_required('group.change_group', raise_exception=True)
def edit_group_permission(request, group_id):
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT permission_id FROM auth_group_permissions where group_id = 1'
    cursor.execute( query )
    group_permissions = cursor.fetchall()
    group_permissions_js = json.dumps(group_permissions)

    query = 'SELECT * FROM auth_permission'
    cursor.execute( query )
    permission = cursor.fetchall()

    context = {
        'group_permissions' : group_permissions, 
        'group_permissions_js' : group_permissions_js, 
        
        'permissions' : permission,
    }
    return render(request, 'group_permission.html', context)

def get_auth_permission(group_id):
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT permission_id FROM auth_group_permissions where group_id = ' + str(group_id)
    cursor.execute( query )
    current_permission_list = [group_permissions['permission_id'] for group_permissions in cursor.fetchall()]
    return current_permission_list 

def update_group_permission(request, group_id):

    #list permission awal dari DB
    current_permission_list = get_auth_permission(group_id)
    print("ori = ", current_permission_list )


    #list permission yang di check di table
    new_permission_list = request.POST.getlist('check_permission', False)
    new_permission_list = list(map(int, new_permission_list))
    print("new = ", new_permission_list )

    #list permission yang baru ditambah di compare sama DB
    addded_perm = list(set(new_permission_list) - set(current_permission_list))
    print("addded perm = ", addded_perm)

    #list permission yang baru didelete di compare sama DB
    deleted_perm = list(set(current_permission_list) -set(new_permission_list))
    print("deleted perm = ", deleted_perm)

    for perm in addded_perm:
        query = f"INSERT INTO AUTH_GROUP_PERMISSIONS VALUES(null, {group_id}, {perm} )"
        with connection.cursor() as cursor:
            cursor.execute(query)

    for perm in deleted_perm:
        query = f"DELETE FROM AUTH_GROUP_PERMISSIONS WHERE GROUP_ID = {group_id} AND PERMISSION_ID = {perm}"
        with connection.cursor() as cursor:
            cursor.execute(query)

    # query = f"SELECT NAME FROM AUTH_GROUP WHERE ID = " + str(group_id)
    # with connection.cursor() as cursor:
    #     cursor.execute(query)
    messages.add_message(request, messages.SUCCESS, "Permission Updated Sucessfully")
    return redirect('/group')

def group_user(request, group_id):
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM auth_user_groups JOIN auth_user ON auth_user.id = auth_user_groups.user_id where group_id = ' + str(group_id)
    cursor.execute( query )
    group_user = cursor.fetchall()

    
    query = 'SELECT * FROM auth_group where id = ' + str(group_id)
    cursor.execute( query )
    group_detail = cursor.fetchone()


    context = {
        'group_user' : group_user, 
        'group_detail' : group_detail
    }
    return render(request, 'group_user.html', context)