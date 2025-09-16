from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required


@login_required(login_url="institut_app:login")
def ListeEcheancierSpecial(request):
    pass

@login_required(login_url="institut_app:login")
def ApiValidateEcheancierSpecial(request):
    pass