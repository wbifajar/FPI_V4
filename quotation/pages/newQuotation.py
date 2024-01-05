from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
import json

import sys
sys.path.append("..")

from ..databaseConnect import *


@login_required
@permission_required('quotation.add_quotation', raise_exception=True)
def CreateNewQuotation(request):
	connection = connect()
	cursor = connection.cursor(dictionary=True)

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

	cursor.execute('select * from set_quotation')
	set_quotation = cursor.fetchall()
	set_quotationjs = json.dumps(set_quotation)

	cursor.execute('SELECT process.*, category_process.categoryName FROM process LEFT JOIN category_process ON process.CategoryId = category_process.idCategory')
	dropProcess = cursor.fetchall()
	dropProcessjs = json.dumps(dropProcess)

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
		'set_quotation' : set_quotation[0],
		'set_quotationjs' : set_quotationjs,
		'dropProcess' : dropProcess,
		'dropProcessjs' : dropProcessjs,
	}

	if request.method == 'POST':
		processLength = request.POST.get('processLength')
		print(processLength)
		
    

	return render(request, 'createquotation.html', context)

# def line_graph(request):
#     if request.method == 'POST':
#         # Get the user input from the form
#         graphQuantity = request.POST.getlist('graphQuantity')
#         BudgetPerUnit = request.POST.getlist('BudgetPerUnit')
        
#         # Convert the input values to integers
#         graphQuantity = list(map(int, graphQuantity))
#         BudgetPerUnit = list(map(int, BudgetPerUnit))
        
#         # Create the line graph
#         plt.plot(graphQuantity, BudgetPerUnit)
#         plt.xlabel('X-axis')
#         plt.ylabel('Y-axis')
#         plt.title('Line Graph')
        
#         # Save the graph to a temporary image file
#         graph_path = 'myapp/static/myapp/line_graph.png'
#         plt.savefig(graph_path)
        
#         # Pass the graph path to the template
#         context = {'graph_path': graph_path}
        
#         # Render the template with the graph
#         return render(request, 'myapp/line_graph.html', context)

#     # Render the empty form
#     return render(request, 'myapp/input_form.html')
