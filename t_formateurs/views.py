from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def ListFormateur(request):
    return HttpResponse('<h1>Liste des formateurs</h1>')