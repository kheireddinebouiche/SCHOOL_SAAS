from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import *
from ..forms import *
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django_tenants.utils import get_tenant_model, schema_context
from django.http import JsonResponse
from django.db.models import Q



login_required(login_url="institut_app:login")
def PageFormateurs(request):
    liste = Formateurs.objects.all()
    context = {
        "formateurs" : liste
    }
    return render(request, 'tenant_folder/formateur/liste_des_formateur.html', context)

@login_required(login_url="institut_app:login")
def create_formateur(request):
    pass