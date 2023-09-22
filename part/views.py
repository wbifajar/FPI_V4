from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.db import connection
from .databaseConnect import *
# Create your views here.

def part(request):

    return render(request, 'part.html')
