from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json

import sys
sys.path.append("..")

from ..databaseConnect import *

connection = connect()
cursor = connection.cursor(dictionary=True)

@login_required
def CreateNewQuotation(request):

	cursor.execute('select * from process')
	process = cursor.fetchall()
	processjs = json.dumps(process)

	cursor.execute('select * from other')
	others = cursor.fetchall()
	othersjs = json.dumps(others)

	cursor.execute('select * from customer')
	customer = cursor.fetchall()
	customerjs = json.dumps(customer)

	cursor.execute('select * from product')
	product = cursor.fetchall()
	productjs = json.dumps(product)

	cursor.execute('select * from part')
	part = cursor.fetchall()
	partjs = json.dumps(part)

	context = {
		'process' : process,
		'processjs' : processjs,
		'others' : others,
		'othersjs' : othersjs,
		'customer' : customer,
		'customerjs' : customerjs,
		'product' : product,
		'productjs' : productjs,
		'part' : part,
		'partjs' : partjs,
		'partbar' : part,
		'partbarjs' : partjs,
		'partreflectcost' : part,
		'partreflectcostjs' : partjs,
	}

	if request.method == 'POST':
		processLength = request.POST.get('processLength')
		print(processLength)
		
    

	return render(request, 'createquotation.html', context)