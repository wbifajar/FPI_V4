from django.shortcuts import render

def Quotation(request):
  
  if request.method == 'POST':
    QuotationId = request.POST.get('QuotationId')

  return render(request, 'quotation.html')