from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from ..models import *
from django.contrib.auth.decorators import login_required


@login_required(login_url="institut_app:login")
def ApiLoadEntrepriseData(request):
    pass

@login_required(login_url="institut_app:login")
def ApiUpdateEntrepriseData(request):
    pass


@login_required(login_url="institut_app")
def ApiListeBanckAccountEntreprise(request):
    pass

@login_required(login_url="institut_app")
def ApiSaveBankAccount(request):
    pass




