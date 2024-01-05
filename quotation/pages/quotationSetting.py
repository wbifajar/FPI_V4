from django.shortcuts import render, redirect
import json
from django.contrib.auth.decorators import permission_required
import sys
sys.path.append("..")
from django.db import connection
from ..databaseConnect import *

@permission_required('quosettings.view_quosettings', raise_exception=True)
def QuotationSetting(request):

    connection = connect()
    cursor = connection.cursor(dictionary=True)
    query = 'SELECT * FROM set_quotation'
    cursor.execute( query )
    set_quotation = cursor.fetchall()

    for item in set_quotation:
        item['half_margin_part_scale'] = int(int(item['set_margin_part_scale']) / 2)
        item['half_margin_number_of'] = int(int(item['set_margin_number_of']) / 2)

    context = {
        'set_quotation' : set_quotation[0], 
    }

    return render(request, 'settingquotation.html', context)

@permission_required('quosettings.change_quosettings', raise_exception=True)
def edit(request):

    materialRatePercentage = request.POST.get('materialRatePercentage', False)
    outSourceRatePercentage = request.POST.get('outSourceRatePercentage', False)
    managementCostRatePercentage = request.POST.get('managementCostRatePercentage', False)
    expiredDateDefault = request.POST.get('expiredDateDefault', False)
    exposedPartScaleRate = request.POST.get('exposedPartScaleRate', False)
    marginPartScaleRate = request.POST.get('marginPartScaleRate', False)
    exposedNumOfRate = request.POST.get('exposedNumOfRate', False)
    marginNumOfRate = request.POST.get('marginNumOfRate', False)
    query = f'UPDATE set_quotation \
        SET \
        set_material_rate = "{materialRatePercentage}", \
        set_out_source_rate = "{outSourceRatePercentage}", \
        set_management_cost_rate = "{managementCostRatePercentage}", \
        set_expired_date = "{expiredDateDefault}", \
        set_exposed_part_scale = "{exposedPartScaleRate}", \
        set_margin_part_scale = "{marginPartScaleRate}", \
        set_exposed_number_of = "{exposedNumOfRate}", \
        set_margin_number_of = "{marginNumOfRate}"\
        WHERE idset_quotation = 1'
    print(query)

    with connection.cursor() as cursor:
        cursor.execute(query)
    return redirect('/Quotation/QuotationSetting')

#   return render(request, 'settingquotation.html')   
